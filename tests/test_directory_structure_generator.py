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
    """
    Test the generate method of DirectoryStructureGenerator with different sorting strategies.

    This test uses parameterization to test different combinations of sorting order and case sensitivity.
    It verifies that the directory structure is correctly generated and sorted according to the specified
    sorting strategy. The expected order of files in the output is checked to ensure correctness.

    Args:
        setup_test_dir: A pytest fixture that sets up a test directory structure.
        tmpdir: A pytest fixture that provides a temporary directory unique to the test invocation.
        sort_order: The sorting order ('asc' for ascending, 'desc' for descending).
        case_sensitive: Boolean flag indicating whether sorting is case-sensitive.
        expected_files: The expected order of files in the generated output.
    """
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
        print(output)
        assert output.index(expected_files[0]) < output.index(expected_files[1])
       
def test_generate_with_gitignore(setup_test_dir, tmpdir):
    """
    Test the generate method of DirectoryStructureGenerator with gitignore patterns.

    This test verifies that the directory structure is correctly generated while ignoring
    paths specified by gitignore patterns (like .git and .tmp files). It ensures that
    ignored paths are not present in the generated output.

    Args:
        setup_test_dir: A pytest fixture that sets up a test directory structure.
        tmpdir: A pytest fixture that provides a temporary directory unique to the test invocation.
    """
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
