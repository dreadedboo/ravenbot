import logging

def new_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)