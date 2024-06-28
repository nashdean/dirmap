import pytest
import os
from src.generator.directory_structure_generator import DirectoryStructureGenerator
from src.ignore.path_ignorer import PathIgnorer

@pytest.fixture
def setup_test_dir(tmpdir):
    root_dir = tmpdir.mkdir("test_dir")
    test_file = root_dir.join("file1.txt")
    test_file.write("test file")
    return root_dir.strpath

def test_generate(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer([])
    
    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        assert "├── test_dir/" in f.read()
