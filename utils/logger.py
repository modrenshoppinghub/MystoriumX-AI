"""
MystoriumX AI Studio - Production Logging Module
"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "MystoriumX", log_file: Path = None) -> logging.Logger:
    """Configures and returns a custom logger with formatted console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if logger is already initialized
    if logger.handlers:
        return logger

    # Standard Log Format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler (Outputs to Console / Colab Terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Saves logs to disk if path provided)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
