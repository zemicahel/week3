import logging
import os

def setup_logger(name, log_file='analysis.log'):
    """
    Sets up a logger that writes to both console and a file.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create Console Handler
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(formatter)
    logger.addHandler(c_handler)

    # Create File Handler
    if not os.path.exists('logs'):
        os.makedirs('logs')
    f_handler = logging.FileHandler(os.path.join('logs', log_file))
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)

    return logger