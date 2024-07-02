import logging
import traceback
from typing import Type
from dirmapper.ignore.path_ignorer import PathIgnorer

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger(__name__)

def log_exception(exc: Exception, stacktrace: bool = False) -> None:
    logger.error("An error occurred: %s", exc)
    if stacktrace:
        logger.error("Stack Trace:", exc_info=True)

def log_ignored_paths(ignorer: Type[PathIgnorer]) -> None:
    root_counts = ignorer.get_root_ignored_counts()
    root_directories = ignorer.get_root_directories()
    for root_dir in root_directories:
        logger.info(f"Ignoring {root_counts[root_dir]} paths in root ignored folder '{root_dir}'")
