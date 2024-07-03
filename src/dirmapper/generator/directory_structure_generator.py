import os
import sys
from typing import List, Tuple
from dirmapper.utils.logger import log_exception, logger, log_ignored_paths
from dirmapper.utils.sorting_strategy import NoSortStrategy, AscendingSortStrategy, DescendingSortStrategy
from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.config import STYLE_MAP, EXTENSIONS, FORMATTER_MAP
from dirmapper.styles.base_style import BaseStyle
from dirmapper.formatter.formatter import Formatter

class DirectoryStructureGenerator:
    def __init__(self, root_dir: str, output_file: str, ignorer: PathIgnorer, sort_order: str = None, style: BaseStyle = None, formatter: Formatter = None):
        self.root_dir = root_dir
        self.output_file = output_file
        self.ignorer = ignorer
        self.sort_order = sort_order
        self.style = style if style else STYLE_MAP['tree']()
        self.formatter = formatter if formatter else FORMATTER_MAP['plain']()

        if sort_order == 'asc':
            self.sorting_strategy = AscendingSortStrategy()
        elif sort_order == 'desc':
            self.sorting_strategy = DescendingSortStrategy()
        else:
            self.sorting_strategy = NoSortStrategy()

        self._validate_file_extension()

        logger.info(f"Directory structure generator initialized for root dir: {root_dir}, output file: {output_file}, style: {self.style.__class__.__name__}, formatter: {self.formatter.__class__.__name__}")

    def generate(self) -> None:
        try:
            if not self.verify_path(self.root_dir):
                raise NotADirectoryError(f'"{self.root_dir}" is not a valid path to a directory.')
            logger.info(f"Generating directory structure...")

            sorted_structure = self._build_sorted_structure(self.root_dir, level=0)

            raw_structure = self.style.write_structure(sorted_structure)
            formatted_structure = self.formatter.format(raw_structure)

            with open(self.output_file, 'w') as f:
                f.write(formatted_structure)

            # Log the ignored paths after generating the directory structure
            log_ignored_paths(self.ignorer)

        except NotADirectoryError as e:
            log_exception(e)
            sys.exit(1)
        except Exception as e:
            log_exception(e)
            print(f"Error: {e}")

    def _build_sorted_structure(self, current_dir: str, level: int) -> List[Tuple[str, int, str]]:
        structure = []
        dir_contents = os.listdir(current_dir)
        sorted_contents = self.sorting_strategy.sort(dir_contents)

        for item in sorted_contents:
            item_path = os.path.join(current_dir, item)
            if self.ignorer.should_ignore(item_path):
                continue

            structure.append((item_path, level, item))

            if os.path.isdir(item_path):
                structure.extend(self._build_sorted_structure(item_path, level + 1))

        return structure

    def _validate_file_extension(self) -> None:
        style_name = self.style.__class__.__name__.lower().replace('style', '')
        expected_extension = EXTENSIONS.get(style_name, '.txt')
        if not self.output_file.endswith(expected_extension):
            raise ValueError(f"Output file '{self.output_file}' does not match the expected extension for style '{self.style.__class__.__name__}': {expected_extension}")

    def verify_path(self, path: str = None) -> bool:
        return os.path.isdir(str(path)) if path else os.path.isdir(self.root_dir)
