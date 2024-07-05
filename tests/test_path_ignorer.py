import pytest
from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.ignore.ignore_list_reader import SimpleIgnorePattern, RegexIgnorePattern

def test_should_ignore():
    """
    Test PathIgnorer with SimpleIgnorePattern.

    This test verifies that paths matching the simple ignore patterns (like .git/, .github/, .cache)
    are correctly identified and ignored by the PathIgnorer. It also ensures that paths not matching
    the ignore patterns are not ignored.
    """
    ignorer = PathIgnorer([
        SimpleIgnorePattern('.git/'),
        SimpleIgnorePattern('.github/'),
        SimpleIgnorePattern('.cache')
    ])
    
    assert ignorer.should_ignore('some/path/.git/')
    assert ignorer.should_ignore('some/path/.github/')
    assert ignorer.should_ignore('some/path/.github/objects')
    assert ignorer.should_ignore('some/path/.cache')
    assert not ignorer.should_ignore('some/path/dir')
    assert not ignorer.should_ignore('some/path/file.txt')

def test_should_ignore_regex():
    """
    Test PathIgnorer with RegexIgnorePattern.

    This test verifies that paths matching the regex ignore patterns (like .git and its subdirectories, .cache)
    are correctly identified and ignored by the PathIgnorer. It also ensures that paths not matching
    the regex patterns are not ignored.
    """
    ignorer = PathIgnorer([
        RegexIgnorePattern(r'\.git(/.*)?$'),
        RegexIgnorePattern(r'\.cache')
    ])

    assert ignorer.should_ignore('some/path/.git')
    assert ignorer.should_ignore('some/path/.git/objects')
    assert not ignorer.should_ignore('some/path/.github')
    assert ignorer.should_ignore('some/path/.cache')
    assert not ignorer.should_ignore('some/path/dir')
    assert not ignorer.should_ignore('some/path/file.txt')