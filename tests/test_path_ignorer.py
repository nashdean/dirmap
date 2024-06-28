import pytest
from src.ignore.path_ignorer import PathIgnorer

def test_should_ignore():
    ignorer = PathIgnorer(['ignore_this'])
    
    assert ignorer.should_ignore('ignore_this/path')
    assert not ignorer.should_ignore('do_not_ignore_this/path')
