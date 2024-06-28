import argparse
import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ignore.ignore_list_reader import FileIgnoreListReader
from ignore.path_ignorer import PathIgnorer
from generator.directory_structure_generator import DirectoryStructureGenerator
from utils.logger import logger, log_exception

def main():
    parser = argparse.ArgumentParser(description="Generate a directory structure mapping.")
    parser.add_argument('root_directory', type=str, help="The root directory to map.")
    parser.add_argument('output_file', type=str, help="The output file to save the directory structure.")
    parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    
    args = parser.parse_args()
    
    try:
        ignore_list_reader = FileIgnoreListReader()
        ignore_list = ignore_list_reader.read_ignore_list(args.ignore_file)
        
        if not args.no_gitignore:
            gitignore_list = ignore_list_reader.read_ignore_list('.gitignore')
            ignore_list.extend(gitignore_list)
        
        path_ignorer = PathIgnorer(ignore_list)
        directory_structure_generator = DirectoryStructureGenerator(args.root_directory, args.output_file, path_ignorer)
        
        directory_structure_generator.generate()
        logger.info(f"Directory structure saved to {args.output_file}")
    except Exception as e:
        log_exception(e)

if __name__ == "__main__":
    main()
