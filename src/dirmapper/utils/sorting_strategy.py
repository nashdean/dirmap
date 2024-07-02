from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, items):
        pass

class AscendingSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items)

class DescendingSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items, reverse=True)
