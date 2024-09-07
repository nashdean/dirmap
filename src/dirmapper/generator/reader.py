from dirmapper.ignore.path_ignorer import PathIgnorer
from dirmapper.generator.directory_structure_generator import DirectoryStructureGenerator
from dirmapper.utils.logger import logger, log_exception
from dirmapper.config import STYLE_MAP, FORMATTER_MAP
from dirmapper.utils.cli_utils import read_ignore_patterns, parse_sort_argument
from dirmapper.utils.sorting_strategy import AscendingSortStrategy, DescendingSortStrategy, NoSortStrategy
from dirmapper.writer.writer import write_template

def read_command(args):
    try:
        ignore_patterns = read_ignore_patterns(args.ignore_file, not args.no_gitignore, args.ignore)
        
        path_ignorer = PathIgnorer(ignore_patterns)

        style_class = STYLE_MAP[args.style]()
        formatter_class = FORMATTER_MAP[args.format]()

        # Determine the sorting strategy and case sensitivity
        sort_order, case_sensitive = parse_sort_argument(args.sort)

        if sort_order == 'asc':
            sorting_strategy = AscendingSortStrategy(case_sensitive)
        elif sort_order == 'desc':
            sorting_strategy = DescendingSortStrategy(case_sensitive)
        else:
            sorting_strategy = NoSortStrategy()

        # Instantiate DirectoryStructureGenerator
        directory_structure_generator = DirectoryStructureGenerator(
            args.root_directory, 
            args.output, 
            path_ignorer, 
            sorting_strategy=sorting_strategy, 
            style=style_class, 
            formatter=formatter_class
        )
        directory_structure = directory_structure_generator.generate()

        if args.template:
            write_template(args.template, directory_structure)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(directory_structure)
        logger.info(f"Directory structure saved to {args.output}")
        if args.file_only and not args.output:
            raise ValueError("The --output argument is required when --file_only is specified.")
        
        if not args.file_only:
            print()
            print(directory_structure)
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")
