import argparse
import sys

from dirmapper.generator.reader import read_command
from dirmapper.writer.writer import write_command
from dirmapper.utils.cli_utils import get_package_version
from dirmapper.utils.logger import log_exception
from dirmapper.config import STYLE_MAP, FORMATTER_MAP


def main():
    package_name = "dirmapper"
    version = get_package_version(package_name)

    parser = argparse.ArgumentParser(description="Generate or create a directory structure.")
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {version}', help="Show the version number and exit.")
    
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for reading directory structure
    read_parser = subparsers.add_parser('read', help='Read and generate directory structure')
    read_parser.add_argument('root_directory', type=str, help="The root directory to map.")
    read_parser.add_argument('output_file', type=str, help="The output file to save the directory structure.")
    read_parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    read_parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    read_parser.add_argument('--sort', choices=['asc', 'asc:case', 'desc', 'desc:case'], help="Sort files and folders in ascending (asc) or descending (desc) order. Use ':case' suffix for case-sensitive sorting.")
    read_parser.add_argument('--style', choices=STYLE_MAP.keys(), default='tree', help="Choose the style of the directory structure output.")
    read_parser.add_argument('--format', choices=FORMATTER_MAP.keys(), default='plain', help="Choose the format of the directory structure output.")
    read_parser.add_argument('--ignore', type=str, nargs='*', default=[], help="Additional ignore patterns to exclude.")

    # Subcommand for writing directory structure
    write_parser = subparsers.add_parser('write', help='Write directory structure from template')
    write_parser.add_argument('template_file', type=str, help="The template file to create directory structure from (in YAML or JSON format).")
    write_parser.add_argument('root_directory', type=str, help="The root directory where the structure will be created.")
    write_parser.add_argument('--template', nargs='?', const='generated_template.json', help='Generate a template file in the current working directory (optional: specify the file name)')

    args = parser.parse_args()

    try:
        if args.command == "read":
            read_command(args)
        elif args.command == "write":
            write_command(args)
        else:
            parser.print_help()
            sys.exit(1)
            
    except Exception as exc:
        log_exception(exc, stacktrace=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
