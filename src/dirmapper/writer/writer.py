from dirmapper.writer.structure_writer import StructureWriter
from dirmapper.writer.template_parser import TemplateParser
from dirmapper.utils.logger import log_exception, logger

def write_command(args):
    try:
        template_parser = TemplateParser(args.template_file)
        structure = template_parser.parse_template()
        
        structure_writer = StructureWriter(args.root_directory)
        structure_writer.create_structure(structure)
        
        logger.info(f"Directory structure created from template {args.template_file}")
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")
