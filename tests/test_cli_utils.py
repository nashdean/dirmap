# tests/test_cli_utils.py

import pytest
from dirmapper.utils.cli_utils import read_ignore_patterns, parse_sort_argument, get_package_version
from dirmapper.ignore.ignore_list_reader import IgnorePattern, SimpleIgnorePattern, RegexIgnorePattern
from unittest.mock import patch, MagicMock
from importlib.metadata import PackageNotFoundError  # Add this import


def test_read_ignore_patterns():
    """
    Test the read_ignore_patterns function.

    This test verifies that the read_ignore_patterns function correctly reads ignore patterns from a file,
    includes patterns from .gitignore when specified, and adds additional ignore patterns provided at runtime.
    The test uses mocking to simulate reading from ignore files and checks that the resulting list of patterns
    includes all expected patterns.

    Mocks:
        dirmapper.utils.cli_utils.IgnoreListReader: Mocked to simulate reading ignore patterns from files.

    Asserts:
        The length of the resulting ignore list is as expected.
        The types and values of the patterns in the resulting ignore list are as expected.
    """
    mock_ignore_list_reader = MagicMock()
    mock_ignore_list_reader.read_ignore_list.side_effect = [
        [SimpleIgnorePattern('test1'), RegexIgnorePattern(r'regex1')],
        [SimpleIgnorePattern('test2')]
    ]
    
    additional_ignores = ['additional1', 'regex:additional2']
    with patch('dirmapper.utils.cli_utils.IgnoreListReader', return_value=mock_ignore_list_reader):
        result = read_ignore_patterns('ignore_file', True, additional_ignores)

    assert len(result) == 5
    assert isinstance(result[0], SimpleIgnorePattern)
    assert result[0].pattern == 'test1'
    assert isinstance(result[1], RegexIgnorePattern)
    assert result[1].pattern == 'regex1'
    assert isinstance(result[2], SimpleIgnorePattern)
    assert result[2].pattern == 'test2'
    assert isinstance(result[3], SimpleIgnorePattern)
    assert result[3].pattern == 'additional1'
    assert isinstance(result[4], RegexIgnorePattern)
    assert result[4].pattern == 'additional2'

def test_parse_sort_argument():
    """
    Test the parse_sort_argument function.

    This test verifies that the parse_sort_argument function correctly parses the sort argument
    to determine the sorting strategy and case sensitivity. It checks different possible values
    of the sort argument and ensures that the function returns the expected tuple of sort order
    and case sensitivity.

    Asserts:
        The function returns the expected tuple of sort order and case sensitivity for various inputs.
    """
    assert parse_sort_argument(None) == (None, False)
    assert parse_sort_argument('asc') == ('asc', False)
    assert parse_sort_argument('asc:case') == ('asc', True)
    assert parse_sort_argument('desc') == ('desc', False)
    assert parse_sort_argument('desc:case') == ('desc', True)

def test_get_package_version():
    """
    Test the get_package_version function.

    This test verifies that the get_package_version function correctly retrieves the version of a package.
    It uses mocking to simulate the presence or absence of the package and checks that the function returns
    the expected version string in both cases.

    Mocks:
        dirmapper.utils.cli_utils.version: Mocked to simulate the behavior of importlib.metadata.version.

    Asserts:
        The function returns the correct version string when the package is found.
        The function returns "Unknown version" when the package is not found.
    """
    with patch('dirmapper.utils.cli_utils.version', return_value='1.0.0'):
        assert get_package_version('some_package') == '1.0.0'
    
    with patch('dirmapper.utils.cli_utils.version', side_effect=PackageNotFoundError):
        assert get_package_version('some_package') == 'Unknown version'
