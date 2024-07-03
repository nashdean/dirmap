from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseStyle(ABC):
    @abstractmethod
    def write_structure(self, structure: List[Tuple[str, int]]) -> str:
        pass
