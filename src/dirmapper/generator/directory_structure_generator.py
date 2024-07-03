import os
import sys
from typing import Optional, TextIO
from dirmapper.utils.logger import log_exception, logger, log_ignored_paths
from dirmapper.utils.sorting_strategy import AscendingSortStrategy, DescendingSortStrategy
from dirmapper.ignore.path_ignorer import PathIgnorer

class DirectoryStructureGenerator:
    def __init__(self, root_dir: str, output_file: str, ignorer: PathIgnorer, sort_order: str = 'asc'):
        self.root_dir = root_dir
        self.output_file = output_file
        self.ignorer = ignorer
        self.sorting_strategy = AscendingSortStrategy() if sort_order == 'asc' else DescendingSortStrategy()
        
        logger.info(f"Directory structure generator initialized for root dir: {root_dir} and output file: {output_file}")

    def generate(self) -> None:
        try:
            with open(self.output_file, 'w') as f:
                if not self.verify_path(self.root_dir):
                    raise NotADirectoryError(f'"{self.root_dir}" is not a valid path to a directory.')
                logger.info(f"Generating directory structure to output file...")

                self._write_tree(f, self.root_dir, level=0)

            # Log the ignored paths after generating the directory structure
            log_ignored_paths(self.ignorer)

        except (NotADirectoryError, OSError) as e:
            log_exception(e)
            sys.exit(1)

    def _write_tree(self, f: TextIO, current_dir: str, level: int) -> None:
        try:
            dir_contents = sorted(os.listdir(current_dir), key=self.sorting_strategy.sort)
        except OSError as e:
            logger.error(f"Error reading directory contents: {e}")
            return

        indent = '│   ' * level

        for i, item in enumerate(dir_contents):
            item_path = os.path.join(current_dir, item)
            if self.ignorer.should_ignore(item_path):
                continue

            is_last = (i == len(dir_contents) - 1)
            connector = '└── ' if is_last else '├── '

            if os.path.isdir(item_path):
                f.write(f"{indent}{connector}{item}/\n")
                self._write_tree(f, item_path, level + 1)
            else:
                f.write(f"{indent}{connector}{item}\n")
    
    def verify_path(self, path: Optional[str] = None) -> bool:
        return os.path.isdir(str(path)) if path else os.path.isdir(self.root_dir)
