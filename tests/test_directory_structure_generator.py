import pytest
import os
import sys

# Include the src directory in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dirmapper.generator.directory_structure_generator import DirectoryStructureGenerator
from dirmapper.ignore.path_ignorer import PathIgnorer

@pytest.fixture
def setup_test_dir(tmpdir):
    root_dir = tmpdir.mkdir("test_dir")
    root_dir.mkdir(".git").join("config").write("dummy config")
    root_dir.mkdir(".github").join("workflow").write("dummy workflow")
    root_dir.mkdir("sub_dir").join("file1.txt").write("test file")
    root_dir.join("file2.txt").write("test file")
    root_dir.join("file1.log").write("test log file")
    return root_dir.strpath

@pytest.mark.parametrize("sort_order, expected_files", [
    ("asc", ["file1.log", "file2.txt"]),
    ("desc", ["file2.txt", "file1.log"]),
], ids=["ascending", "descending"])
def test_generate_with_sorting(setup_test_dir, tmpdir, sort_order, expected_files):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer(['.git*/', '*.tmp'])

    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer, sort_order)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        for filename in expected_files:
            assert filename in output
        
        if sort_order == "asc":
            assert output.index("file1.log") < output.index("file2.txt")
        else:
            assert output.index("file2.txt") < output.index("file1.log")

def test_generate_with_gitignore(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer(['.git*/', '*.tmp'])

    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        assert "├── test_dir/" in output
        assert "│   ├── file1.log" in output
        assert "    └── file2.txt" in output
        assert "│   ├── sub_dir/" in output
        assert "│       └── file1.txt" in output
        assert ".git" not in output
        assert ".github" not in output

def test_generate_without_gitignore(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer([])

    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        assert "├── test_dir/" in output
        assert "│   ├── file1.log" in output
        assert "    └── file2.txt" in output
        assert "│   ├── sub_dir/" in output
        assert "│       └── file1.txt" in output
        assert "│   ├── .github/" in output
        assert "│       └── workflow" in output
        assert "│   ├── .git/" in output
        assert "│       └── config" in output
