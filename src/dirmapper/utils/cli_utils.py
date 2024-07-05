# dirmapper/utils/cli_utils.py

from importlib.metadata import version, PackageNotFoundError
from dirmapper.ignore.ignore_list_reader import IgnoreListReader, SimpleIgnorePattern, RegexIgnorePattern
from typing import List, Tuple

def read_ignore_patterns(ignore_file: str, include_gitignore: bool, additional_ignores: str) -> List[str]:
    """
    Reads ignore patterns from the specified ignore file and optionally includes patterns from .gitignore.

    Args:
        ignore_file (str): The path to the ignore file listing directories and files to ignore.
        include_gitignore (bool): Flag indicating whether to include patterns from .gitignore.
        additional_ignores (list): Additional patterns to ignore specified at runtime.

    Returns:
        list: A list of ignore patterns.
    """
    ignore_list_reader = IgnoreListReader()
    ignore_list = ignore_list_reader.read_ignore_list(ignore_file)
    
    if include_gitignore:
        gitignore_list = ignore_list_reader.read_ignore_list('.gitignore')
        ignore_list.extend(gitignore_list)

    # Add additional ignore patterns from the command line
    for pattern in additional_ignores:
        if pattern.startswith('regex:'):
            ignore_list.append(RegexIgnorePattern(pattern[len('regex:'):]))
        else:
            ignore_list.append(SimpleIgnorePattern(pattern))

    return ignore_list

def parse_sort_argument(sort_arg: str) -> Tuple[str, bool]:
    """
    Parses the sort argument to determine the sorting strategy and case sensitivity.

    Args:
        sort_arg (str): The sort argument in the format 'asc', 'asc:case', 'desc', or 'desc:case'.

    Returns:
        tuple: A tuple containing the sort order and case sensitivity flag.
    """
    if sort_arg is None:
        return None, False
    
    parts = sort_arg.split(':')
    sort_order = parts[0]
    case_sensitive = True if len(parts) > 1 and parts[1] == 'case' else False
    return sort_order, case_sensitive

def get_package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Unknown version"
