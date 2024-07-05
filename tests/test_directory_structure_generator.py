import pytest
import os
from dirmapper.generator.directory_structure_generator import DirectoryStructureGenerator
from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.utils.sorting_strategy import AscendingSortStrategy, DescendingSortStrategy, NoSortStrategy
from dirmapper.ignore.ignore_list_reader import SimpleIgnorePattern, RegexIgnorePattern

@pytest.mark.parametrize("sort_order, case_sensitive, expected_files", [
    ("asc", False, ["file1.log", "file2.txt"]),
    ("desc", False, ["file2.txt", "file1.log"]),
    ("asc", True, ["file1.log", "file2.txt"]),
    ("desc", True, ["file2.txt", "file1.log"]),
], ids=["ascending_insensitive", "descending_insensitive", "ascending_sensitive", "descending_sensitive"])
def test_generate_with_sorting(setup_test_dir, tmpdir, sort_order, case_sensitive, expected_files):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer([
        SimpleIgnorePattern('.git*/'), 
        SimpleIgnorePattern('*.tmp')
    ])

    if sort_order == "asc":
        sorting_strategy = AscendingSortStrategy()
    elif sort_order == "desc":
        sorting_strategy = DescendingSortStrategy()
    else:
        sorting_strategy = NoSortStrategy()

    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer, sorting_strategy, case_sensitive)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        for filename in expected_files:
            assert filename in output
        
        print(output.index(expected_files[0]))
        output.index(expected_files[1])
        if sort_order == "asc":
            for i in range(len(expected_files) - 1):
                assert output.index(expected_files[i]) < output.index(expected_files[i + 1])
        else:
            for i in range(len(expected_files) - 1):
                assert output.index(expected_files[i]) > output.index(expected_files[i + 1])


def test_generate_with_gitignore(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer([
        SimpleIgnorePattern('.git'), 
        SimpleIgnorePattern('*.tmp')
    ])

    sorting_strategy = NoSortStrategy()
    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer, sorting_strategy, case_sensitive=True)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        assert "├── .git" not in output
        assert "├── .github" not in output
        assert "├── sub_dir/" in output
        assert "│   └── file1.txt" in output
        assert "├── file2.txt" in output
        assert "└── file1.log" in output

def test_generate_without_gitignore(setup_test_dir, tmpdir):
    output_file = tmpdir.join("test_output.txt").strpath
    path_ignorer = PathIgnorer([])

    sorting_strategy = NoSortStrategy()
    generator = DirectoryStructureGenerator(setup_test_dir, output_file, path_ignorer, sorting_strategy, case_sensitive=True)
    generator.generate()
    
    assert os.path.isfile(output_file)
    with open(output_file) as f:
        output = f.read()
        assert "├── file1.log" in output
        assert "├── file2.txt" in output
        assert "├── sub_dir/" in output
        assert "│   └── file1.txt" in output
        assert "├── .github/" in output
        assert "│   └── workflow" in output
        assert "├── .git/" in output
        assert "│   └── config" in output
