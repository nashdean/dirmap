from utils.logger import logger

class PathIgnorer:
    def __init__(self, ignore_list):
        self.ignore_list = ignore_list
        logger.info(f"Path ignorer initialized with ignore list: {ignore_list}")

    def should_ignore(self, path):
        for ignore in self.ignore_list:
            if ignore in path:
                return True
        return False
