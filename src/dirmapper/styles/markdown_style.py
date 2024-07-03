from typing import List, Tuple
import os
from dirmapper.styles.base_style import BaseStyle

class MarkdownStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int, str]]) -> str:
        result = []
        for item_path, level, item in structure:
            indent = '    ' * level
            if os.path.isdir(item_path):
                result.append(f"{indent}- {item}/")
            else:
                result.append(f"{indent}- {item}")
        return '\n'.join(result)
