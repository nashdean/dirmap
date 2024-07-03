from typing import List, Tuple
import os
from dirmapper.styles.base_style import BaseStyle

class TreeStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int]]) -> str:
        result = []
        for i, (item_path, level) in enumerate(structure):
            indent = '│   ' * level
            is_last = (i == len(structure) - 1 or structure[i + 1][1] < level)
            connector = '└── ' if is_last else '├── '

            if os.path.isdir(item_path):
                result.append(f"{indent}{connector}{os.path.basename(item_path)}/")
            else:
                result.append(f"{indent}{connector}{os.path.basename(item_path)}")
        
        return '\n'.join(result)
