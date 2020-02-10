import logging
import os
from unittest.mock import patch
from tool.cucumbers import Cucumbers
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
    # assert bdd.framework is 'pytest_bdd'
    assert bdd.framework is 'behave'
    assert len(bdd.feature_files)
    assert len(bdd.step_files)
