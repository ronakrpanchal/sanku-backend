import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from rich.logging import RichHandler
import os

# testing pre commit hook
def get_logger(
    name: Optional[str] = None,
    log_file: str = "app.log",
    log_dir: str = "logs",
    log_level: str = logging.INFO,
    show_time: bool = True,
    show_level: bool = True,
    show_path: bool = True,
    rich_tracebacks: bool = True,
) -> logging.Logger:
    logger_name = name or __name__
    logger = logging.getLogger(logger_name)
    os.makedirs(log_dir, exist_ok=True)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file), maxBytes=1_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)

    rich_handler = RichHandler(
        show_time=show_time,
        show_level=show_level,
        show_path=show_path,
        rich_tracebacks=rich_tracebacks,
    )
    logger.addHandler(file_handler)
    logger.addHandler(rich_handler)

    return logger
