import os
from dirmapper.utils.logger import logger

class StructureWriter:
    """
    Class to create directory structures from a template.
    """
    def __init__(self, base_path: str):
        self.base_path = base_path

    def create_structure(self, structure: dict):
        """
        Create the directory structure from the template.
        """
        if 'meta' not in structure or 'template' not in structure:
            raise ValueError("Template must contain 'meta' and 'template' sections.")
        
        meta = structure['meta']
        template = structure['template']

        if 'version' not in meta or meta['version'] != '1.1':
            raise ValueError("Unsupported template version. Supported version is '1.1'.")
        
        # Log or use additional meta tags if needed
        author = meta.get('author', 'Unknown')
        description = meta.get('description', 'No description provided')
        creation_date = meta.get('creation_date', 'Unknown')
        last_modified = meta.get('last_modified', 'Unknown')
        license = meta.get('license', 'No license specified')

        logger.info(f"Creating structure by author, {author}")
        logger.debug(f"Description: {description}")
        logger.debug(f"Creation date: {creation_date}")
        logger.info(f"Template Last modified: {last_modified}")
        logger.debug(f"License: {license}")
        logger.info(f"Creating directory structure at root directory: {self.base_path}")

        self._create_structure_from_template(self.base_path, template)

    def _create_structure_from_template(self, base_path: str, structure: dict):
        """
        Recursively create the directory structure (makes directories and files) from the template.
        """
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, list):
                os.makedirs(path, exist_ok=True)
                for item in content:
                    if isinstance(item, dict):
                        self._create_structure_from_template(path, item)
            else:
                # Ensure the directory exists before creating the file
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write('')  # Create an empty file
