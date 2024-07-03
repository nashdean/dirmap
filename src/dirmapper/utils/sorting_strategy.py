from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, items):
        pass

class NoSortStrategy(SortingStrategy):
    def sort(self, items):
        return items
        
class AscendingSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items)

class DescendingSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items, reverse=True)
