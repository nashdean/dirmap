from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, items, case_sensitive: bool = True):
        pass

class NoSortStrategy(SortingStrategy):
    def sort(self, items, case_sensitive: bool = True):
        return items

class AscendingSortStrategy(SortingStrategy):
    def sort(self, items, case_sensitive: bool = True):
        if not case_sensitive:
            return sorted(items, key=str.lower)
        return sorted(items)

class DescendingSortStrategy(SortingStrategy):
    def sort(self, items, case_sensitive: bool = True):
        if not case_sensitive:
            return sorted(items, key=str.lower, reverse=True)
        return sorted(items, reverse=True)
