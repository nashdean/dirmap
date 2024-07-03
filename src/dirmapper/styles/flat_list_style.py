from typing import List, Tuple
from dirmapper.styles.base_style import BaseStyle

class FlatListStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int]]) -> str:
        result = []
        for item_path, level in structure:
            result.append(item_path)
        return '\n'.join(result)
