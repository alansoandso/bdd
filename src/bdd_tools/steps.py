#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import logging
import os
import re
from contextlib import suppress
import behave
from behave.parser import ParserError
from behave.model import Scenario
from typing import Iterator
from bdd_tools.step import Step


logging.basicConfig(format='%(message)s')


class Steps(object):
    def __init__(self):
        self.steps = []
        self.actions = collections.defaultdict(int)

    def __str__(self):
        """
        :return: Report on step definitions:
                    {action}: {usage count}
        """
        stats = '\nSteps by type:\n'
        for action, count in self.actions.items():
            stats += f'{action}: {count}\n'
        return stats

    def __len__(self):
        return len(self.steps)

    def items(self) -> Iterator[Step]:
        for i in self.steps:
            yield i

    def ranking(self) -> Iterator[Step]:
        """
        :return: Iterator of steps by increasing usage counts
        """
        for r in sorted(self.steps, key=lambda s: s.count, reverse=False):
            yield r

    def append(self, step):
        """Add step to maintained list
        """
        self.steps.append(step)
        self.actions[step.action] += 1

    def report(self):
        """
        :return: Report on step ordered by usage in feature files
        """
        out = '\n'.join([s.__str__() for s in self.ranking()])
        out += f'\nTotal number of steps executed by all features: {sum([s.count for s in self.steps])}\n'
        return out

    def unused_steps_files(self):
        """
        :return: a list of files which have unused steps definitions
        """
        files = set([s.path for s in self.steps if s.count == 0])
        return list(files)

    def unused_steps_line_nbr(self, path) -> Iterator[int]:
        """
        :return: Iterator of line numbers in a step definition file not used in features
        """
        for line_nbr in [s.line_no for s in self.steps if s.path == path and s.count == 0]:
            yield line_nbr

    def parse_feature(self, lines):
        """ Update the steps usage count for each matching line
        """
        for line in lines:
            line = line.strip()
            for step in self.items():
                if step.tally(line):
                    break
            else:
                logging.warning(f'Missing step for: {line}')

    def parse_steps(self, file_path):
        """parse for steps e.g.:
            @Then("^number of viewed content is (?:within limits|less than )(.*)$")
            @given(parsers.parse('I playout "{asset}"'), target_fixture='cli')
            @then('the result page will include "{text}"')
        """
        rgx = re.compile(r'@?(?P<action>([Gg]iven|[Ww]hen|[Tt]hen|[Aa]nd|[Bb]ut)).*\([\"\']'
                         r'(?P<step>.*?)[\"\']\).*')

        with open(file_path) as f:
            for line_nbr, line in enumerate(f):
                matching = rgx.fullmatch(line.strip())
                if matching:
                    self.append(Step(matching.group('action'), matching.group('step'), line_nbr, file_path))

    def process_feature(self, file_path):
        """Ignoring anything tagged with @pending, tally up the step usage counts
        """
        feature_file = ''.join(open(file_path).readlines())
        lines = []
        with suppress(ParserError):
            feature = behave.parser.parse_feature(feature_file, filename=os.path.basename(file_path))
            if not feature:
                return
            logging.debug(f'{file_path}')
            scenarios = feature.walk_scenarios()
            for scn in scenarios:
                if isinstance(scn, Scenario):
                    if 'pending' in scn.tags:
                        logging.debug(f'{scn.name}: {scn.tags}')
                        continue
                    if scn.background:
                        lines += [s.name for s in scn.background_steps]
                    lines += [s.name for s in scn.steps]

            self.parse_feature(lines)
