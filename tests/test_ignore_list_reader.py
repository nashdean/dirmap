import pytest
from src.dirmapper.ignore.ignore_list_reader import IgnoreListReader, SimpleIgnorePattern, RegexIgnorePattern

def test_read_ignore_list(tmpdir):
    """
    Test the read_ignore_list method of IgnoreListReader.

    This test creates a temporary .mapping-ignore file with both simple and regex ignore patterns.
    It verifies that the read_ignore_list method correctly reads these patterns and returns a list
    of the appropriate pattern objects (SimpleIgnorePattern and RegexIgnorePattern).

    Args:
        tmpdir: A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    ignore_file = tmpdir.join('.mapping-ignore')
    ignore_file.write("ignore_this\nregex:^ignore_\n")

    reader = IgnoreListReader()
    ignore_list = reader.read_ignore_list(ignore_file.strpath)
    
    assert isinstance(ignore_list, list)
    assert len(ignore_list) == 2
    assert isinstance(ignore_list[0], SimpleIgnorePattern)
    assert isinstance(ignore_list[1], RegexIgnorePattern)
    assert ignore_list[0].pattern == "ignore_this"
    assert ignore_list[1].pattern == "^ignore_"
