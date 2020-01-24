#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import fnmatch
import os
import re
from contextlib import suppress

from behave import parser
from behave.model import Scenario


class Steps:
    def __init__(self):
        self.steps = []
        self.actions = collections.defaultdict(int)
        self.unused = []

    def __str__(self):
        """
        :return: Report on step definitions by type
        """
        repr = '\nSteps by type:\n'
        for action, count in self.actions.items():
            repr += '{}: {}\n'.format(action, count)
        return repr

    def __len__(self):
        return len(self.steps)

    def items(self):
        for i in self.steps:
            yield i

    def ranking(self):
        for r in sorted(self.steps, key=lambda s: s.count, reverse=False):
            yield r

    def append(self, step):
        self.steps.append(step)
        self.actions[step.action] += 1

    def report(self):
        """

        :return: Report on step usage in feature files
        """
        out = '\n'.join([s.__str__() for s in self.ranking()])
        out += '\nTotal number of steps executed by all features: {}\n'.format(sum([s.count for s in self.steps]))
        return out

    def unused_stepdef_files(self):
        # a set of paths which have unused steps defs
        files = set([s.path for s in self.steps if s.count == 0])
        return list(files)

    def unused_stepdef_lineno(self, path):
        for line_no in [s.line_no for s in self.steps if s.path == path and s.count == 0]:
            yield line_no


class Step:
    def __init__(self, action, name, line_no, path):
        self.count = 0
        self.action = action
        self.path = path
        self.line_no = line_no
        # lose the \\d+
        name = name.replace('\\"', '"')
        name = name.replace('\\\\', '\\')
        # lose "^<- these bits -->:$"
        # e.g. '"^error code (\\d+) with:$"' to 'error code (\d+) with'
        self.name = name.strip('"').lstrip('^').rstrip('$').rstrip(':')
        self.rgx = re.compile(self.name)

    def __str__(self):
        if self.count == 0:
            return '{}#{} {}'.format(os.path.basename(self.path),  self.line_no, self.name)
        return '{:03} {}'.format(self.count, self.name)

    def __repr__(self):
        return ' '.join([self.action, self.name])

    def tally(self, line):
        """
        Tally up a matching line
        :param line:
        :return: regex match
        """
        if self.rgx.match(line):
            self.count += 1
            return self.count


def find_features(directory, steps) -> Steps:
    """
    Recurse from directory downwards for feature files,
    Return steps tallied with matching lines
    :rtype : Steps
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
                scenarios = feature.walk_scenarios()
                for scn in scenarios:
                    if isinstance(scn, Scenario):
                        if scn.background:
                            lines += [s.name for s in scn.background_steps]
                        lines += [s.name for s in scn.steps]

                parse_feature(lines, steps)

    return steps


def parse_feature(lines, steps):
    """
    Update the steps usage count for each matching line
    """
    for line in lines:
        line = line.strip()
        for step in steps.items():
            if step.tally(line):
                break
        else:
            print('Missing step for: {}'.format(line))

    return steps


def find_step_defs(directory) -> Steps:
    """
    Recurse from directory downwards for matching step files,
    which are parsed for step definitions
    :rtype : Steps
    """
    rgx = re.compile('@?(?P<action>(Given|When|Then|And|But))\((?P<step>".*?")\).*')
    new_steps = Steps()
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in files:
            if filename.endswith(('scala', 'java')):
                fp = os.path.join(path, filename)
                with open(fp) as f:
                    for lineno, line in enumerate(f):
                        matching = rgx.fullmatch(line.strip())
                        if matching:
                            new_steps.append(Step(matching.group('action'), matching.group('step'), lineno, fp))
    return new_steps


