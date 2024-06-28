from ignore.ignore_list_reader import FileIgnoreListReader
from ignore.path_ignorer import PathIgnorer
from generator.directory_structure_generator import DirectoryStructureGenerator
from utils.logger import logger, log_exception

if __name__ == "__main__":
    try:
        root_directory = 'root-dir-goes-here'  # Change this to your root directory
        output_file = 'directory_structure.txt'
        ignore_file = '.mapping-ignore'

        ignore_list_reader = FileIgnoreListReader()
        ignore_list = ignore_list_reader.read_ignore_list(ignore_file)
        path_ignorer = PathIgnorer(ignore_list)
        directory_structure_generator = DirectoryStructureGenerator(root_directory, output_file, path_ignorer)
        
        directory_structure_generator.generate()
        logger.info(f"Directory structure saved to {output_file}")
    except Exception as e:
        log_exception(e,stacktrace=True)