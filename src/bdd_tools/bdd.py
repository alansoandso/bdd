#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from bdd_tools.cucumbers import Cucumbers

logging.basicConfig(format='%(name)s: %(message)s', level=logging.DEBUG)
logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


def get_parser():
    parser = argparse.ArgumentParser(description='BDD steps usage report tool')
    parser.add_argument('-c', '--counts', action="store_true", default=False,
                        help='usage counts, step parser and location')
    parser.add_argument('-u', '--unused', action="store_true", default=False,
                        help='unused steps')
    parser.add_argument('--directory', action="store", nargs='?', default='/Users/alan/workspace/popcorn-qa-cucumber-jvm/src/test',
                        help='starting directory')
    parser.add_argument('search', action="store", nargs='?',
                        help='search for a step that matches a scenario line')

    return parser


def command_line_runner(argv=None):
    parser = get_parser()
    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        parser.print_usage()
        return

    args = parser.parse_args(argv[1:])
    logging.debug(args)

    cucumbers = Cucumbers(args.directory)
    cucumbers.map_steps()
    cucumbers.step_usage()
    print('*'*50)
    print(cucumbers.steps)
    print('*'*50)
    print(cucumbers.steps.report())


if __name__ == '__main__':
    command_line_runner()
