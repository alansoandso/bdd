#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import fnmatch
import logging
import os
import re
from contextlib import suppress
from behave import parser
from behave.model import Scenario
from typing import Iterator
from tool.step import Step


logging.basicConfig(format='%(message)s')


class Steps:
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

    def find_features(self, directory):
        """ Recurse from a directory downwards for feature files
        Ignoring anything tagged with @pending, tally up the usage steo counts
        """
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in fnmatch.filter(files, '*feature'):
                fp = os.path.join(path, filename)
                feature_file = ''.join(open(fp).readlines())
                lines = []
                with suppress(parser.ParserError):
                    feature = parser.parse_feature(feature_file, filename=filename)
                    if not feature:
                        break
                    logging.debug(f'{fp}')
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

    def find_step_definitions(self, directory):
        """Recurse from directory downwards for matching step files,
        which are parsed for step definitions
        """
        # rgx = re.compile(r'@?(?P<action>(Given|When|Then|And|But))\((?P<step>".*?")\).*')
        rgx = re.compile(r'@?(?P<action>([Gg]iven|[Ww]hen|[Tt]hen|[Aa]nd|[Bb]ut))\((?P<step>["\'].*?["\'])\).*')
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in files:
                if filename.endswith(('java', 'py', 'scala')):
                    fp = os.path.join(path, filename)
                    with open(fp) as f:
                        for line_nbr, line in enumerate(f):
                            matching = rgx.fullmatch(line.strip())
                            if matching:
                                self.append(Step(matching.group('action'), matching.group('step'), line_nbr, fp))
