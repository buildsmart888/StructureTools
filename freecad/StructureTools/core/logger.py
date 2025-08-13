"""Project-wide logging helper."""
from __future__ import annotations
import logging
import os
from functools import lru_cache

LOG_LEVEL = os.getenv("STRUCTURETOOLS_LOG_LEVEL", "INFO").upper()

@lru_cache(maxsize=64)
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
        logger.propagate = False
    return logger

__all__ = ["get_logger"]
