import argparse
from ignore.ignore_list_reader import FileIgnoreListReader
from ignore.path_ignorer import PathIgnorer
from generator.directory_structure_generator import DirectoryStructureGenerator
from utils.logger import logger, log_exception

def main(root_directory, output_file, ignore_file, use_gitignore):
    try:
        ignore_list_reader = FileIgnoreListReader()
        ignore_list = ignore_list_reader.read_ignore_list(ignore_file)
        
        if use_gitignore:
            gitignore_list = ignore_list_reader.read_ignore_list('.gitignore')
            ignore_list.extend(gitignore_list)
        
        path_ignorer = PathIgnorer(ignore_list)
        directory_structure_generator = DirectoryStructureGenerator(root_directory, output_file, path_ignorer)
        
        directory_structure_generator.generate()
        logger.info(f"Directory structure saved to {output_file}")
    except Exception as e:
        log_exception(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a directory structure mapping.")
    parser.add_argument('root_directory', type=str, help="The root directory to map.")
    parser.add_argument('output_file', type=str, help="The output file to save the directory structure.")
    parser.add_argument('--ignore_file', type=str, default='.mapping-ignore', help="The ignore file listing directories and files to ignore.")
    parser.add_argument('--no_gitignore', action='store_true', help="Do not include patterns from .gitignore.")
    
    args = parser.parse_args()
    
    main(args.root_directory, args.output_file, args.ignore_file, not args.no_gitignore)
