from unittest.mock import patch
from tool import bdd
import logging
LOG = logging.getLogger(__name__)


@patch('sys.argv', ['bdd'])
def test_cli_usage(capsys):
    """Test if command_line_runner shows help when called without parameters."""
    bdd.command_line_runner()
    out, err = capsys.readouterr()
    assert 'usage: bdd [-h]' in out


@patch('sys.argv', ['bdd', '-c'])
def test_cli(capsys):
    """Test command_line_runner with a parameter"""
    bdd.command_line_runner()
    out, err = capsys.readouterr()
    LOG.info(out)
    assert 'Steps by type:' in out


@patch('sys.argv', ['bdd', '--directory', '/Users/alan/Dropbox/python/python3/playable/tests', '-c'])
def test_cli_directory(capsys):
    """Test command_line_runner with a parameter"""
    bdd.command_line_runner()
    out, err = capsys.readouterr()
    LOG.info(out)

# bdd --thens
# Step and paths
# user should not have any current offers       # WinBackStepDefs.java:41
# Found 274 "Then" steps

# bdd --unused
# unused steps
# Number of unused Given steps: 0 out of 279 avaliable steps
# Number of unused Then steps: 0 out of 274 avaliable steps
# Number of unused When steps: 0 out of 328 avaliable steps

# bdd --counts
# 0896:  I expect status code (.*)             # RestClientStepDefs.java:127
# Number of Given steps available: 279
# Number of Then steps available: 274
# Number of When steps available: 328

