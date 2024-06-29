import os
import sys
from dirmapper.utils.logger import log_exception
from dirmapper.utils.logger import logger

class DirectoryStructureGenerator:
    def __init__(self, root_dir, output_file, ignorer):
        self.root_dir = root_dir
        self.output_file = output_file
        self.ignorer = ignorer
        logger.info(f"Directory structure generator initialized for root dir: {root_dir} and output file: {output_file}")

    def generate(self):
        try:
            with open(self.output_file, 'w') as f:
                if not self.verify_path(self.root_dir):
                    raise NotADirectoryError(f'"{self.root_dir}" is not a valid path to a directory.')
                logger.info(f"Generating directory structure to output file...")
                for dirpath, dirnames, filenames in os.walk(self.root_dir):
                    if self.ignorer.should_ignore(dirpath):
                        continue

                    level = dirpath.replace(self.root_dir, '').count(os.sep)
                    indent = '│   ' * level
                    sub_indent = '│   ' * (level + 1)
                    f.write('{}├── {}/\n'.format(indent, os.path.basename(dirpath)))

                    # Copy dirnames list to avoid modifying it while iterating
                    for dirname in list(dirnames):
                        full_dirname = os.path.join(dirpath, dirname)
                        if self.ignorer.should_ignore(full_dirname):
                            dirnames.remove(dirname)

                    for i, filename in enumerate(filenames):
                        full_filename = os.path.join(dirpath, filename)
                        if self.ignorer.should_ignore(full_filename):
                            continue

                        file_indent = sub_indent if i < len(filenames) - 1 else sub_indent[:-4] + '    '
                        connector = '├── ' if i < len(filenames) - 1 else '└── '
                        f.write('{}{}{}\n'.format(file_indent, connector, filename))
        except NotADirectoryError as e:
            log_exception(e)
            sys.exit(1)
    
    def verify_path(self, path=None):
        if path is not None:
            return os.path.isdir(str(path))
        return os.path.isdir(self.root_dir)
