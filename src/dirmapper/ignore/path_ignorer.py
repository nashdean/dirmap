import re
from dirmapper.utils.logger import logger

class PathIgnorer:
    def __init__(self, ignore_list):
        self.ignore_patterns = [self._convert_pattern(pattern) for pattern in ignore_list]
        
    def _convert_pattern(self, pattern):
        pattern = pattern.strip()
        if pattern.endswith('/'):
            pattern = pattern[:-1] + '(/.*)?'
        pattern = pattern.replace('.', r'\.').replace('*', r'.*')
        return pattern

    def should_ignore(self, path):
        for pattern in self.ignore_patterns:
            if re.search(pattern, path):
                logger.info(f"Ignoring path: {path}")
                return True
        return False
