#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from bdd import steps
from bdd import purge


def main():
    if len(sys.argv) == 2 and sys.argv[1].endswith(('--help', '-h')):
        print('Usage: {} [-h] [directory]\nFind and report on step usage within the feature files'.format(os.path.basename(sys.argv[0])))
    if len(sys.argv) == 2:
        p = sys.argv[1]
    else:
        p = '.'

    # p = '/Users/alan/workspace/qa-cucumber-jvm/src/test'
    # p = '/Users/alan/workspace/plutus-partner-accounts/partner-accounts-test/src/test'
    p = '/Users/alan/workspace/umc-integration-tests/src'

    step_defs = steps.find_step_defs(p)
    steps.find_features(p, step_defs)
    # Show step usage counts
    print(step_defs)
    print(step_defs.report())
    # Modify the unused stepdef with @@ to highlight it is ready to purge
    # for path in step_defs.unused_stepdef_files():
    #     print(path)
    #     purge.purge_stepdefs(path, step_defs)


if __name__ == '__main__':
    main()
