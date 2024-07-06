import os

class StructureWriter:
    """
    Class to create directory structures from a template.
    """
    def __init__(self, base_path: str):
        self.base_path = base_path

    def create_structure(self, structure: dict):
        self._create_structure_from_template(self.base_path, structure)

    def _create_structure_from_template(self, base_path: str, structure: dict):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self._create_structure_from_template(path, content)
            elif isinstance(content, list):
                os.makedirs(path, exist_ok=True)
                for item in content:
                    item_path = os.path.join(path, item)
                    if isinstance(item, dict):
                        self._create_structure_from_template(path, item)
                    else:
                        with open(item_path, 'w') as f:
                            f.write("")  # Create an empty file
            else:
                with open(path, 'w') as f:
                    f.write("")  # Create an empty file
