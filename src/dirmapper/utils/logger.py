import logging
import traceback

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger(__name__)

def log_exception(exc, stacktrace=False):
    logger.error("An error occurred: %s", exc)
    if stacktrace:
        logger.error("Stack Trace:", exc_info=True)

def log_ignored_paths(ignore_counts):
    for directory, count in ignore_counts.items():
        logger.info(f"Ignoring {count} paths in folder '{directory}'")
