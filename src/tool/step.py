import logging
import os
import re

logging.basicConfig(format='%(message)s')


class Step:
    def __init__(self, action, name, line_nbr, path):
        self.count = 0
        self.action = action
        self.path = path
        self.line_no = line_nbr
        # lose the \\d+
        name = name.replace('\\"', '"')
        name = name.replace('\\\\', '\\')
        # lose "^<- these bits -->:$"
        # e.g. '"^error code (\\d+) with:$"' to 'error code (\d+) with'
        self.name = name.strip('"').lstrip('^').rstrip('$').rstrip(':')
        self.rgx = re.compile(self.name)

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


