import pytest
from dirmapper.ignore.path_ignorer import PathIgnorer

def test_should_ignore():
    ignorer = PathIgnorer(['.git/', '.github/', '.*cache'])
    
    assert ignorer.should_ignore('some/path/.git')
    assert ignorer.should_ignore('some/path/.github')
    assert ignorer.should_ignore('some/path/.cache')
    assert not ignorer.should_ignore('some/path/dir')
    assert not ignorer.should_ignore('some/path/file.txt')

def test_should_ignore_regex():
    ignorer = PathIgnorer(['.git*/', '.*cache'])

    assert ignorer.should_ignore('some/path/.git')
    assert ignorer.should_ignore('some/path/.git/objects')
    assert ignorer.should_ignore('some/path/.github')
    assert ignorer.should_ignore('some/path/.cache')
    assert not ignorer.should_ignore('some/path/dir')
    assert not ignorer.should_ignore('some/path/file.txt')
