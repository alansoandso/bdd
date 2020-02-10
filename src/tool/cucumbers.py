import logging
import os
import re
from tool.steps import BehaveSteps
from tool.step import Step

logging.basicConfig(format='%(message)s')


class Cucumbers:
    """Model of the Cucumber test files
    """
    def __init__(self, path=''):
        self.path = path
        self.framework = ''
        self.step_files = []
        self.feature_files = []
        self.steps = None
        if path:
            self.find_files(path)

    def __str__(self):
        return f'Framework: {self.framework}'

    def find_files(self, directory):
        """Recurse from directory downwards for step and feature files,
        """
        self.path = directory
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in files:
                fp = os.path.join(path, filename)
                if filename.endswith('feature'):
                    self.feature_files.append(fp)
                if filename.endswith(('java', 'py')):
                    self.step_files.append(fp)
                    self.determine_framework(fp)

    def determine_framework(self, file_path):
        if not self.framework:
            with open(file_path) as step_file:
                for line in step_file:
                    if 'from pytest_bdd' in line:
                        self.framework = 'behave'
                        return
                    if 'from behave' in line:
                        self.framework = 'behave'
                        self.steps = BehaveSteps()
                        return
                    if 'import cucumber.api.java' in line:
                        self.framework = 'behave'
                        return

    def map_steps(self):
        for fp in self.step_files:
            self.steps.parse_steps(fp)
