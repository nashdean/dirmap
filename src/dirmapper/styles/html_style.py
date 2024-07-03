from typing import List, Tuple
import os
from dirmapper.styles.base_style import BaseStyle

class HTMLStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int, str]]) -> str:
        result = ['<ul>']
        previous_level = -1

        for item_path, level, item in structure:
            if level > previous_level:
                result.append('<ul>')
            elif level < previous_level:
                result.append('</ul>' * (previous_level - level))

            relative_path = os.path.relpath(item_path, start=structure[0][0])
            if os.path.isdir(item_path):
                result.append(f'<li><a href="{relative_path}">{item}/</a></li>')
            else:
                result.append(f'<li><a href="{relative_path}">{item}</a></li>')

            previous_level = level

        result.append('</ul>' * (previous_level + 1))
        return '\n'.join(result)
