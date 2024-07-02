import re
import os
from collections import defaultdict

class PathIgnorer:
    def __init__(self, ignore_list):
        self.ignore_patterns = [self._convert_pattern(pattern) for pattern in ignore_list]
        self.ignore_counts = defaultdict(int)  # To keep track of ignored paths per directory
        self.root_ignored_counts = defaultdict(int)  # To keep track of ignored paths per root directory
        self.root_directories = set()

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
                self._increment_root_ignore_count(path)
                return True
        return False

    def _increment_ignore_count(self, path):
        directory = os.path.dirname(path)
        self.ignore_counts[directory] += 1

    def _increment_root_ignore_count(self, path):
        root_directory = self._find_root_directory(path)
        self.root_ignored_counts[root_directory] += 1

    def _find_root_directory(self, path):
        for pattern in self.ignore_patterns:
            match = re.match(pattern, path)
            if match:
                root_dir = match.group().split('/')[0]
                self.root_directories.add(root_dir)
                return root_dir
        return os.path.dirname(path)

    def get_ignore_counts(self):
        return self.ignore_counts

    def get_root_ignored_counts(self):
        return self.root_ignored_counts

    def get_root_directories(self):
        return self.root_directories
