import yaml
import json

class TemplateParser:
    """
    Class to parse template files in YAML or JSON format.
    """
    def __init__(self, template_file: str):
        self.template_file = template_file

    def parse_template(self) -> dict:
        with open(self.template_file, 'r') as f:
            if self.template_file.endswith('.yaml') or self.template_file.endswith('.yml'):
                return yaml.safe_load(f)
            elif self.template_file.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Unsupported template file format. Please use YAML or JSON.")
