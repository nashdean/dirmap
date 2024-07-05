import argparse
import sys

from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.generator.directory_structure_generator import DirectoryStructureGenerator
from dirmapper.utils.logger import logger, log_exception
from dirmapper.config import STYLE_MAP, FORMATTER_MAP
from dirmapper.utils.cli_utils import read_ignore_patterns, parse_sort_argument, get_package_version
from dirmapper.utils.sorting_strategy import AscendingSortStrategy, DescendingSortStrategy, NoSortStrategy

def main():
    package_name = "dirmapper"
    version = get_package_version(package_name)

    parser = argparse.ArgumentParser(description="Generate a directory structure mapping.")
    parser.add_argument('root_directory', type=str, help="The root directory to map.")
    parser.add_argument('output_file', type=str, help="The output file to save the directory structure.")
    parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    parser.add_argument('--sort', choices=['asc', 'asc:case', 'desc', 'desc:case'], help="Sort files and folders in ascending (asc) or descending (desc) order. Use ':case' suffix for case-sensitive sorting.")
    parser.add_argument('--style', choices=STYLE_MAP.keys(), default='tree', help="Choose the style of the directory structure output.")
    parser.add_argument('--format', choices=FORMATTER_MAP.keys(), default='plain', help="Choose the format of the directory structure output.")
    parser.add_argument('--ignore', type=str, nargs='*', default=[], help="Additional ignore patterns to exclude.")
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {version}', help="Show the version number and exit.")
    
    args = parser.parse_args()

    try:
        ignore_patterns = read_ignore_patterns(args.ignore_file, not args.no_gitignore, args.ignore)
        
        path_ignorer = PathIgnorer(ignore_patterns)

        style_class = STYLE_MAP[args.style]()
        formatter_class = FORMATTER_MAP[args.format]()

        # Determine the sorting strategy and case sensitivity
        sort_order, case_sensitive = parse_sort_argument(args.sort)

        if sort_order == 'asc':
            sorting_strategy = AscendingSortStrategy()
        elif sort_order == 'desc':
            sorting_strategy = DescendingSortStrategy()
        else:
            sorting_strategy = NoSortStrategy()

        # Instantiate DirectoryStructureGenerator
        directory_structure_generator = DirectoryStructureGenerator(
            args.root_directory, 
            args.output_file, 
            path_ignorer, 
            sorting_strategy=sorting_strategy, 
            case_sensitive=case_sensitive,
            style=style_class, 
            formatter=formatter_class
        )
        
        directory_structure_generator.generate()
        logger.info(f"Directory structure saved to {args.output_file}")
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
