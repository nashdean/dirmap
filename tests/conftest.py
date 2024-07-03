# tests/fixtures.py

import pytest
import os
import sys

# Include the src directory in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def setup_test_dir(tmpdir):
    root_dir = tmpdir.mkdir("test_dir")
    root_dir.mkdir(".git").join("config").write("dummy config")
    root_dir.mkdir(".github").join("workflow").write("dummy workflow")
    root_dir.mkdir("sub_dir").join("file1.txt").write("test file")
    root_dir.join("file2.txt").write("test file")
    root_dir.join("file1.log").write("test log file")
    return root_dir.strpath
