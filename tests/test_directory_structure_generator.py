import pytest
import os
from src.generator.directory_structure_generator import DirectoryStructureGenerator
from src.ignore.path_ignorer import PathIgnorer

@pytest.fixture
def setup_test_dir(tmpdir):
    root_dir = tmpdir.mkdir("test_dir")
    root_dir.mkdir(".git").join("config").write("dummy config")
    root_dir.mkdir(".github").join("workflow").write("dummy workflow")
    root_dir.mkdir("sub_dir").join("file1.txt").write("test file")
    root_dir.join("file2.txt").write("test file")
    return root_dir.strpath

def test_generate_with_gitignore(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer(['.git*/', '*.tmp'])

    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        assert "├── test_dir/" in output
        assert "└── sub_dir/" in output
        assert "    ├── file1.txt" in output
        assert "├── file2.txt" in output
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
        assert "├── .git/" in output
        assert "├── .github/" in output
        assert "└── sub_dir/" in output
        assert "    ├── file1.txt" in output
        assert "├── file2.txt" in output
