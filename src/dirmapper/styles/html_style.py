from typing import List, Tuple
import os
from dirmapper.styles.base_style import BaseStyle

class HTMLStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int]]) -> str:
        result = ['<ul>']
        previous_level = -1

        for item_path, level in structure:
            if level > previous_level:
                result.append('<ul>' * (level - previous_level))
            elif level < previous_level:
                result.append('</ul>' * (previous_level - level))
            
            if os.path.isdir(item_path):
                result.append(f'<li>{os.path.basename(item_path)}/</li>')
            else:
                result.append(f'<li>{os.path.basename(item_path)}</li>')

            previous_level = level

        result.append('</ul>' * (previous_level + 1))
        return '\n'.join(result)
