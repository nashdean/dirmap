import pytest
from src.dirmapper.ignore.ignore_list_reader import FileIgnoreListReader

def test_read_ignore_list(tmpdir):
    ignore_file = tmpdir.join('.mapping-ignore')
    ignore_file.write("ignore_this\nignore_that\n")
    
    reader = FileIgnoreListReader()
    ignore_list = reader.read_ignore_list(ignore_file.strpath)
    
    assert isinstance(ignore_list, list)
    assert 'ignore_this' in ignore_list
    assert 'ignore_that' in ignore_list
