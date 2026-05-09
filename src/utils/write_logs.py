import logging
import os

def setup_logger(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    return logging.getLogger("zap")

def log_info(logger, message):
    logger.info(message)

def log_warning(logger, message):
    logger.warning(message)

def log_error(logger, message):
    logger.error(message)

def log_debug(logger, message):
    logger.debug(message)