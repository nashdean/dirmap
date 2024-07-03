import os
from typing import List, Tuple
from dirmapper.styles.base_style import BaseStyle

class JSONStyle(BaseStyle):
    def write_structure(self, structure: List[Tuple[str, int, str]]) -> dict:
        def build_json_structure(structure, level):
            result = {}
            i = 0
            while i < len(structure):
                item_path, item_level, item = structure[i]
                if item_level == level:
                    if os.path.isdir(item_path):
                        sub_structure, sub_items = build_json_structure(structure[i+1:], level + 1)
                        result[item] = sub_structure
                        i += sub_items
                    else:
                        result[item] = item_path
                elif item_level < level:
                    break
                i += 1
            return result, i

        json_structure, _ = build_json_structure(structure, 0)
        return json_structure
