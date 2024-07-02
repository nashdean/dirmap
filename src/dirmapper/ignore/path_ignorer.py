import re
import os
from collections import defaultdict

class PathIgnorer:
    def __init__(self, ignore_list):
        self.ignore_patterns = [self._convert_pattern(pattern) for pattern in ignore_list]
        self.ignore_counts = defaultdict(int)  # To keep track of ignored paths per directory
        
    def _convert_pattern(self, pattern):
        pattern = pattern.strip()
        if pattern.endswith('/'):
            pattern = pattern[:-1] + '(/.*)?'
        pattern = pattern.replace('.', r'\.').replace('*', r'.*')
        return pattern

    def should_ignore(self, path):
        for pattern in self.ignore_patterns:
            if re.search(pattern, path):
                self._increment_ignore_count(path)
                return True
        return False

    def _increment_ignore_count(self, path):
        directory = os.path.dirname(path)
        self.ignore_counts[directory] += 1
