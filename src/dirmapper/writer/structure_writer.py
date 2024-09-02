import os
from dirmapper.utils.logger import logger

class StructureWriter:
    """
    Class to create directory structures from a template.
    """
    def __init__(self, base_path: str):
        self.base_path = base_path

    def create_structure(self, structure: dict):
        if 'meta' not in structure or 'template' not in structure:
            raise ValueError("Template must contain 'meta' and 'template' sections.")
        
        meta = structure['meta']
        template = structure['template']

        if 'version' not in meta or meta['version'] != '1.0':
            raise ValueError("Unsupported template version. Supported version is '1.0'.")
        
        # Log or use additional meta tags if needed
        author = meta.get('author', 'Unknown')
        description = meta.get('description', 'No description provided')
        creation_date = meta.get('creation_date', 'Unknown')
        last_modified = meta.get('last_modified', 'Unknown')
        license = meta.get('license', 'No license specified')

        logger.info(f"Creating structure by {author}")
        logger.debug(f"Description: {description}")
        logger.debug(f"Creation date: {creation_date}")
        logger.info(f"Template Last modified: {last_modified}")
        logger.debug(f"License: {license}")

        self._create_structure_from_template(self.base_path, template)

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
