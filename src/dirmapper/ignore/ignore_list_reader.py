from typing import List
import re

class IgnorePattern:
    """
    Base class for ignore patterns.
    
    Attributes:
        pattern (str): The pattern to ignore.
    """
    def __init__(self, pattern: str):
        self.pattern = pattern

    def matches(self, path: str) -> bool:
        """
        Check if the given path matches the ignore pattern.
        
        Args:
            path (str): The path to check against the pattern.
        
        Returns:
            bool: True if the path matches the pattern, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class SimpleIgnorePattern(IgnorePattern):
    """
    Class for simple ignore patterns.
    """
    def matches(self, path: str) -> bool:
        """
        Check if the given path contains the pattern.
        
        Args:
            path (str): The path to check.
        
        Returns:
            bool: True if the path contains the pattern, False otherwise.
        """
        return self.pattern in path

class RegexIgnorePattern(IgnorePattern):
    """
    Class for regex-based ignore patterns.
    
    Attributes:
        regex (Pattern): Compiled regex pattern.
    """
    def __init__(self, pattern: str):
        super().__init__(pattern)
        self.regex = re.compile(pattern)

    def matches(self, path: str) -> bool:
        """
        Check if the given path matches the regex pattern.
        
        Args:
            path (str): The path to check.
        
        Returns:
            bool: True if the path matches the regex pattern, False otherwise.
        """
        return bool(self.regex.match(path))

class IgnoreListReader:
    """
    Class to read ignore patterns from a file.
    """
    def read_ignore_list(self, ignore_file: str) -> List[IgnorePattern]:
        """
        Read ignore patterns from a file.
        
        Args:
            ignore_file (str): The file containing ignore patterns.
        
        Returns:
            List[IgnorePattern]: A list of ignore pattern objects.
        """
        with open(ignore_file, 'r') as f:
            lines = f.readlines()

        ignore_patterns = []
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line.startswith('regex:'):
                ignore_patterns.append(RegexIgnorePattern(line[len('regex:'):]))
            else:
                ignore_patterns.append(SimpleIgnorePattern(line))

        return ignore_patterns
