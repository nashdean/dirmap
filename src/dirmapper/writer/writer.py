import json
import os
from dirmapper.writer.structure_writer import StructureWriter
from dirmapper.writer.template_parser import TemplateParser
from dirmapper.utils.logger import log_exception, logger

import json
import os
import yaml
from dirmapper.writer.structure_writer import StructureWriter
from dirmapper.writer.template_parser import TemplateParser
from dirmapper.utils.logger import log_exception, logger

def write_command(args):
    try:
        template_parser = TemplateParser(args.template_file)
        if args.template_file.endswith('.txt'):
            with open(args.template_file, 'r') as file:
                structure_str = file.read()
            structure = template_parser.parse_directory_structure(structure_str)
        else:
            structure = template_parser.parse_template()
        
        if not isinstance(structure['template'], dict):
            raise ValueError("Parsed template is not a dictionary")

        structure_writer = StructureWriter(args.root_directory)
        structure_writer.create_structure(structure)
        
        logger.info(f"Directory structure created from template {args.template_file}")
        
        if args.template:
            write_template(args.template, structure)
        
    except Exception as e:
        log_exception(e)
        print(f"Error - writer.py: {e}")

def write_template(template_path, structure):
    """
    Write the generated directory structure to a template file.
    """
    if not template_path.endswith('.json') and not template_path.endswith('.yaml') and not template_path.endswith('.yml'):
        template_path += '.json'  # Default to JSON if no valid extension is provided
    
    with open(template_path, 'w') as template_file:
        if template_path.endswith('.yaml') or template_path.endswith('.yml'):
            yaml.dump(structure, template_file, default_flow_style=False)
        else:
            json.dump(structure, template_file, indent=4)
    logger.info(f"Template file created at {template_path}")