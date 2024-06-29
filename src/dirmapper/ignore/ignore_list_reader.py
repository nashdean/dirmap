import os
from abc import ABC, abstractmethod
from dirmapper.utils.logger import logger

class IgnoreListReader(ABC):
    @abstractmethod
    def read_ignore_list(self, ignore_file):
        pass

class FileIgnoreListReader(IgnoreListReader):
    def read_ignore_list(self, ignore_file):
        logger.info(f"Reading ignore list from {ignore_file}")
        if not os.path.isfile(ignore_file):
            logger.warning(f"Ignore file {ignore_file} not found")
            return []
        with open(ignore_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
