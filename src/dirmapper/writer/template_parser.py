import yaml
import json
import os
import datetime
class TemplateParser:
    """
    Class to parse template files in YAML or JSON format.
    """
    def __init__(self, template_file: str):
        self.template_file = template_file

    def parse_template(self) -> dict:
        with open(self.template_file, 'r') as f:
            if self.template_file.endswith('.yaml') or self.template_file.endswith('.yml'):
                template = yaml.safe_load(f)
            elif self.template_file.endswith('.json'):
                template = json.load(f)
            else:
                raise ValueError("Unsupported template file format. Please use YAML or JSON.")
        
        # Add author, creation_date, and last_modified to meta if not present
        if 'meta' not in template:
            template['meta'] = {}
        if 'author' not in template['meta']:
            template['meta']['author'] = os.getlogin()
        if 'tool' not in template['meta']:
            template['meta']['tool'] = 'dirmapper'
        if 'creation_date' not in template['meta']:
            template['meta']['creation_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'last_modified' not in template['meta']:
            template['meta']['last_modified'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return template
    
    def parse_directory_structure(self, structure_str: str) -> dict:
        lines = structure_str.split('\n')
        template = {}
        stack = [template]
        root_adjusted = False

        if lines and lines[0].strip().endswith('/'):
            root_name = lines[0].strip().rstrip('/')
            template[root_name] = {}
            stack.append(template[root_name])
            root_adjusted = True
            lines = lines[1:]

        for line in lines:
            if not line.strip():
                continue
            if root_adjusted:
                indent_level = (len(line) - len(line.lstrip('│ '))) // 4 + 1  # Adjust indent level to account for root
            else:
                indent_level = (len(line) - len(line.lstrip('│ '))) // 4
            name = line.strip('│ ').strip('├── ').strip('└── ')
            if name.endswith('/'):
                name = name[:-1]
                new_dir = {}
                stack[indent_level][name] = new_dir
                if len(stack) > indent_level + 1:
                    stack[indent_level + 1] = new_dir
                else:
                    stack.append(new_dir)
            else:
                stack[indent_level][name] = ""

        # Get current OS user
        current_user = os.getlogin()

        # Get current date and time
        current_datetime = datetime.datetime.now().isoformat()
        return {
        "meta": {
            "version": "1.0",
            "tool": "dirmapper",
            "author": current_user,
            "creation_date": current_datetime,
            "last_modified": current_datetime  
        },
        "template": template
    }
