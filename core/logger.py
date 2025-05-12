# core/logger.py
import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    filename="logs.txt",
    filemode="a",
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[{func.__name__}] called.")
        return func(*args, **kwargs)
    return wrapper
