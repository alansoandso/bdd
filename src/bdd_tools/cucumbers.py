import logging
import os
import re
from bdd_tools.steps import Steps

logging.basicConfig(format='%(message)s')


class Cucumbers:
    """Model of the Cucumber test files
    """
    def __init__(self, path=''):
        self.path = path
        self.step_files = []
        self.feature_files = []
        self.steps = Steps()
        if path:
            self.find_files(path)

    def __str__(self):
        return f'Features: {len(self.feature_files)}'

    def find_files(self, directory):
        """Look recursively for step and feature files
        """
        self.path = directory
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in files:
                fp = os.path.join(path, filename)
                if filename.endswith('feature'):
                    self.feature_files.append(fp)
                if filename.endswith(('java', 'py')):
                    self.step_files.append(fp)

    def map_steps(self):
        for fp in self.step_files:
            self.steps.parse_steps(fp)

    def step_usage(self):
        for fp in self.feature_files:
            self.steps.process_feature(fp)