import logging
import os
import re
from unittest.mock import patch
from bdd.cucumbers import Cucumbers
from pprint import pformat

LOG = logging.getLogger(__name__)


# @patch('sys.argv', ['bdd'])
def test_find_pytest_bdd():
    """Construct a model of the pytest_bdd files
    """
    bdd = Cucumbers()
    # current files directory + pytest_bdd files
    bdd.find_files(os.path.join(os.path.dirname(__file__), 'pytest_bdd_features'))
    LOG.info(pformat(bdd.__dict__))
    assert len(bdd.feature_files)
    assert len(bdd.step_files)

    bdd.map_steps()
    bdd.step_usage()
    LOG.info(pformat(bdd.steps.__dict__))
    LOG.info(bdd.steps.report())


def test_parse_steps():
    """Playground for re
    """
    steps = [
        '@Then("^number of viewed content is (?:within limits|less than )(.*)$")',
        '@given(parsers.parse(\'I playout "{asset}"\'), target_fixture=\'cli\')',
        '@then(\'the result page will include "{text}"\')',
        r'@When("^I get the products( including kids too|)$")',
        r'@And("Count of (\d+)")'
    ]
    rgx = re.compile(r'@?(?P<action>([Gg]iven|[Ww]hen|[Tt]hen|[Aa]nd|[Bb]ut)).*\([\"\']'
                     r'(?P<step>.*?)[\"\']\).*')
    for line in steps:
        matching = rgx.fullmatch(line.strip())
        if matching:
            print(f"[{matching.group('action')}], <{matching.group('step')}>")

