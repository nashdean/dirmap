import os
import sys
from typing import List, Tuple
from dirmapper.utils.logger import log_exception, logger, log_ignored_paths
from dirmapper.utils.sorting_strategy import NoSortStrategy, AscendingSortStrategy, DescendingSortStrategy
from dirmapper.ignore.path_ignorer import PathIgnorer

class DirectoryStructureGenerator:
    def __init__(self, root_dir: str, output_file: str, ignorer: PathIgnorer, sort_order: str = None):
        self.root_dir = root_dir
        self.output_file = output_file
        self.ignorer = ignorer
        
        if sort_order == 'asc':
            self.sorting_strategy = AscendingSortStrategy()
        elif sort_order == 'desc':
            self.sorting_strategy = DescendingSortStrategy()
        else:
            self.sorting_strategy = NoSortStrategy()

        logger.info(f"Directory structure generator initialized for root dir: {root_dir} and output file: {output_file}")

    def generate(self) -> None:
        try:
            if not self.verify_path(self.root_dir):
                raise NotADirectoryError(f'"{self.root_dir}" is not a valid path to a directory.')
            logger.info(f"Generating directory structure...")

            sorted_structure = self._build_sorted_structure(self.root_dir, level=0)

            with open(self.output_file, 'w') as f:
                self._write_structure(f, sorted_structure)

            # Log the ignored paths after generating the directory structure
            log_ignored_paths(self.ignorer)

        except NotADirectoryError as e:
            log_exception(e)
            sys.exit(1)

    def _build_sorted_structure(self, current_dir: str, level: int) -> List[Tuple[str, int]]:
        structure = []
        dir_contents = os.listdir(current_dir)
        sorted_contents = self.sorting_strategy.sort(dir_contents)

        for item in sorted_contents:
            item_path = os.path.join(current_dir, item)
            if self.ignorer.should_ignore(item_path):
                continue

            structure.append((item_path, level))

            if os.path.isdir(item_path):
                structure.extend(self._build_sorted_structure(item_path, level + 1))

        return structure

    def _write_structure(self, f, structure: List[Tuple[str, int]]) -> None:
        for i, (item_path, level) in enumerate(structure):
            indent = '│   ' * level
            is_last = (i == len(structure) - 1 or structure[i + 1][1] < level)
            connector = '└── ' if is_last else '├── '

            if os.path.isdir(item_path):
                f.write(f"{indent}{connector}{os.path.basename(item_path)}/\n")
            else:
                f.write(f"{indent}{connector}{os.path.basename(item_path)}\n")

    def verify_path(self, path: str = None) -> bool:
        return os.path.isdir(str(path)) if path else os.path.isdir(self.root_dir)
