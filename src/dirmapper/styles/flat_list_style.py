from typing import List, Tuple
from dirmapper.styles.base_style import BaseStyle

class FlatListStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int, str]]) -> str:
        result = [item_path for item_path, _, _ in structure]
        return '\n'.join(result)
