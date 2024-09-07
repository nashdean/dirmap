# directory_structure_generator.py

import os
import sys
from typing import List, Tuple
from dirmapper.utils.logger import log_exception, logger, log_ignored_paths
from dirmapper.utils.sorting_strategy import SortingStrategy
from dirmapper.ignore.ignore_list_reader import IgnoreListReader
from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.config import STYLE_MAP, EXTENSIONS, FORMATTER_MAP
from dirmapper.styles.base_style import BaseStyle
from dirmapper.formatter.formatter import Formatter

class DirectoryStructureGenerator:
    """
    Class to generate a directory structure mapping.
    
    Attributes:
        root_dir (str): The root directory to map.
        output (str): The output file to save the directory structure.
        ignorer (PathIgnorer): Object to handle path ignoring.
        sort_order (str): The order to sort the directory structure ('asc', 'desc', or None).
        style (BaseStyle): The style to use for the directory structure output.
        formatter (Formatter): The formatter to use for the directory structure output.
        sorting_strategy (SortingStrategy): The strategy to use for sorting.
    """
    def __init__(self, root_dir: str, output: str, ignorer: PathIgnorer, sorting_strategy: SortingStrategy, case_sensitive: bool = True, style: BaseStyle = None, formatter: Formatter = None):
        self.root_dir = root_dir
        self.output = output
        self.ignorer = ignorer
        self.sorting_strategy = sorting_strategy
        self.style = style if style else STYLE_MAP['tree']()
        self.formatter = formatter if formatter else FORMATTER_MAP['plain']()

        if output:
            self._validate_file_extension()

        logger.info(f"Directory structure generator initialized for root dir: {root_dir}, output file: {output}, style: {self.style.__class__.__name__}, formatter: {self.formatter.__class__.__name__}")

    def generate(self) -> None:
        """
        Generate the directory structure and write it to the output file.
        
        Raises:
            NotADirectoryError: If the root directory is not valid.
            Exception: If any other error occurs during generation.
        """
        try:
            if not self.verify_path(self.root_dir):
                raise NotADirectoryError(f'"{self.root_dir}" is not a valid path to a directory.')
            logger.info(f"Generating directory structure...")

            sorted_structure = self._build_sorted_structure(self.root_dir, level=0)

            raw_structure = self.style.write_structure(sorted_structure)
            formatted_structure = self.formatter.format(raw_structure) #FIXME: json formatter does not work

            # Log the ignored paths after generating the directory structure
            log_ignored_paths(self.ignorer)

            return formatted_structure

        except NotADirectoryError as e:
            log_exception(e)
            sys.exit(1)
        except Exception as e:
            log_exception(e)
            print(f"Error: {e}")

    def _build_sorted_structure(self, current_dir: str, level: int) -> List[Tuple[str, int, str]]:
        """
        Build the sorted directory structure.
        
        Args:
            current_dir (str): The current directory to build the structure from.
            level (int): The current level of depth in the directory structure.
        
        Returns:
            List[Tuple[str, int, str]]: The sorted directory structure.
        """
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
        """
        Validate the output file extension based on the selected style.
        
        Raises:
            ValueError: If the output file extension does not match the expected extension for the selected style.
        """
        style_name = self.style.__class__.__name__.lower().replace('style', '')
        expected_extension = EXTENSIONS.get(style_name, '.txt')
        if not self.output.endswith(expected_extension):
            raise ValueError(f"Output file '{self.output}' does not match the expected extension for style '{self.style.__class__.__name__}': {expected_extension}")

    def verify_path(self, path: str = None) -> bool:
        """
        Verify if a path is a valid directory.
        
        Args:
            path (str): The path to verify.
        
        Returns:
            bool: True if the path is a valid directory, False otherwise.
        """
        return os.path.isdir(str(path)) if path else os.path.isdir(self.root_dir)
