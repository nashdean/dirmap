import argparse
import sys

from dirmapper.ai.summarizer import summarize_command
from dirmapper.generator.reader import read_command
from dirmapper.writer.writer import write_command
from dirmapper.utils.cli_utils import get_package_version
from dirmapper.utils.logger import log_exception
from dirmapper.config import STYLE_MAP, FORMATTER_MAP

def main():
    parser = argparse.ArgumentParser(description="Dirmapper CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    # Read command
    read_parser = subparsers.add_parser('read', help='Read and generate directory structure')
    read_parser.add_argument('root_directory', type=str, help="The root directory to map.")
    read_parser.add_argument('--template', nargs='?', const='generated_template.json', help='Generate a template file in the current working directory (optional: specify the file name)')
    read_parser.add_argument('--output', type=str, help="The output file to save the directory structure.")
    read_parser.add_argument('--file_only', action='store_true', help="Output only the directory structure to the console.")
    read_parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    read_parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    read_parser.add_argument('--sort', choices=['asc', 'asc:case', 'desc', 'desc:case'], help="Sort files and folders in ascending (asc) or descending (desc) order. Use ':case' suffix for case-sensitive sorting.")
    read_parser.add_argument('--style', choices=STYLE_MAP.keys(), default='tree', help="Choose the style of the directory structure output.")
    read_parser.add_argument('--format', choices=FORMATTER_MAP.keys(), default='plain', help="Choose the format of the directory structure output.")
    read_parser.add_argument('--ignore', type=str, nargs='*', default=[], help="Additional ignore patterns to exclude.")

    # Summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize directory structure")
    summarize_parser.add_argument("input_file", type=str, help="Input file containing the directory structure")
    summarize_parser.add_argument("--format", type=str, choices=["minimalist", "plain", "html", "json"], default="minimalist", help="Format of the summary")
    summarize_parser.add_argument("--output", type=str, help="Output file to save the summary")

    # Write command
    write_parser = subparsers.add_parser("write", help="Write directory structure from template")
    write_parser.add_argument("template_file", type=str, help="Template file to create the directory structure")
    write_parser.add_argument("root_directory", type=str, help="Root directory to create the structure in")
    write_parser.add_argument('--template', nargs='?', const='generated_template.json', help='Generate a template file in the current working directory (optional: specify the file name)')

    args = parser.parse_args()

    try:
        if args.command == "read":
            read_command(args)
        elif args.command == "summarize":
            summarize_command(args)
        elif args.command == "write":
            write_command(args)
        else:
            parser.print_help()
    except Exception as e:
        log_exception(e)
        print(f"Error - main.py: {e}")

if __name__ == "__main__":
    main()