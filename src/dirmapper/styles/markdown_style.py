from typing import List, Tuple
import os
from dirmapper.styles.base_style import BaseStyle

class MarkdownStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int]]) -> str:
        result = []
        for item_path, level in structure:
            indent = '    ' * level
            if os.path.isdir(item_path):
                result.append(f"{indent}- {os.path.basename(item_path)}/")
            else:
                result.append(f"{indent}- {os.path.basename(item_path)}")
        return '\n'.join(result)
