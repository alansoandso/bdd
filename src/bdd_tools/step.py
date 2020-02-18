import logging
import os
import re

logging.basicConfig(format='%(message)s')
LOG = logging.getLogger(__name__)


class Step:
    def __init__(self, action, name, line_nbr, path):
        self.count = 0
        self.action = action.capitalize()
        self.path = path
        self.line_no = line_nbr
        name = name.replace('\\\\', '\\').replace('\\"', '"')
        name = name.lstrip('^').rstrip('$').rstrip(':')
        self.name = name

        try:
            pattern = re.sub('[{<].*[}>]', '.*', name)
            self.rgx = re.compile(pattern)
        except re.error:
            logging.error(f'Error on: {name}')

    def __str__(self):
        return f'{self.count:04}: {self.name:150s}{os.path.basename(self.path)}#{self.line_no}'

    def __repr__(self):
        return f'{self.action} {self.name}'

    def tally(self, line) -> int:
        """Tally up a matching line
        :param line:
        :return: Current tally
        """
        if self.rgx.match(line):
            self.count += 1
            return self.count


