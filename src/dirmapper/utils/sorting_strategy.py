from abc import ABC, abstractmethod
from dirmapper.utils.logger import logger

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, items, case_sensitive: bool = True):
        pass

class NoSortStrategy(SortingStrategy):
    def __init__(self):
        logger.info('No sorting strategy set.')

    def sort(self, items):
        return items

class AscendingSortStrategy(SortingStrategy):
    def __init__(self, case_sensitive: bool = True):
        self.case_sensitive = case_sensitive
        logger.info(f'Sorting strategy set to Ascending order. Sorting is {"case sensitive" if self.case_sensitive else "not case sensitive"}.')

    def sort(self, items):
        if not self.case_sensitive:
            return sorted(items, key=str.lower)
        return sorted(items)

class DescendingSortStrategy(SortingStrategy):
    def __init__(self, case_sensitive: bool = True):
        self.case_sensitive = case_sensitive
        logger.info(f'Sorting strategy set to Descending order. Case sensitivity is {"case sensitive" if self.case_sensitive else "not case sensitive"}.')

    def sort(self, items):
        if not self.case_sensitive:
            return sorted(items, key=str.lower, reverse=True)
        return sorted(items, reverse=True)
