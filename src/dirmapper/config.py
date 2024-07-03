# dirmapper/config.py

from dirmapper.styles.tree_style import TreeStyle
from dirmapper.styles.indentation_style import IndentationStyle
from dirmapper.styles.flat_list_style import FlatListStyle
from dirmapper.styles.markdown_style import MarkdownStyle
from dirmapper.styles.html_style import HTMLStyle
from dirmapper.styles.json_style import JSONStyle
from dirmapper.formatter.formatter import PlainTextFormatter, HTMLFormatter, JSONFormatter

STYLE_MAP = {
    'tree': TreeStyle,
    'indentation': IndentationStyle,
    'flat_list': FlatListStyle,
    'markdown': MarkdownStyle,
    'html': HTMLStyle,
    'json': JSONStyle
}

FORMATTER_MAP = {
    'plain': PlainTextFormatter,
    'html': HTMLFormatter,
    'json': JSONFormatter
}

EXTENSIONS = {
    'tree': '.txt',
    'indentation': '.txt',
    'flat_list': '.txt',
    'markdown': '.md',
    'html': '.html',
    'json': '.json'
}
