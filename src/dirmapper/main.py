import argparse
import sys

from dirmapper.utils.version import get_package_version
from dirmapper.ignore.ignore_list_reader import IgnoreListReader, SimpleIgnorePattern, RegexIgnorePattern
from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.generator.directory_structure_generator import DirectoryStructureGenerator
from dirmapper.utils.logger import logger, log_exception
from dirmapper.config import STYLE_MAP, FORMATTER_MAP

def read_ignore_patterns(ignore_file: str, include_gitignore: bool, additional_ignores: list) -> list:
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

def main():
    package_name = "dirmapper"
    version = get_package_version(package_name)

    parser = argparse.ArgumentParser(description="Generate a directory structure mapping.")
    parser.add_argument('root_directory', type=str, help="The root directory to map.")
    parser.add_argument('output_file', type=str, help="The output file to save the directory structure.")
    parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    parser.add_argument('--ignore', type=str, nargs='*', default=[], help="Additional ignore patterns to exclude.")
    parser.add_argument('--sort', choices=['asc', 'desc'], help="Sort files and folders in ascending (asc) or descending (desc) order. Default is no sorting.")
    parser.add_argument('--style', choices=STYLE_MAP.keys(), default='tree', help="Choose the style of the directory structure output.")
    parser.add_argument('--format', choices=FORMATTER_MAP.keys(), default='plain', help="Choose the format of the directory structure output.")
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {version}', help="Show the version number and exit.")
    
    args = parser.parse_args()

    try:
        ignore_patterns = read_ignore_patterns(args.ignore_file, not args.no_gitignore, args.ignore)
        path_ignorer = PathIgnorer(ignore_patterns)

        style_class = STYLE_MAP[args.style]()
        formatter_class = FORMATTER_MAP[args.format]()

        # Instantiate DirectoryStructureGenerator
        directory_structure_generator = DirectoryStructureGenerator(args.root_directory, args.output_file, path_ignorer, args.sort, style_class, formatter_class)
        
        directory_structure_generator.generate()
        logger.info(f"Directory structure saved to {args.output_file}")
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
