"""Logging utilities for the simulation."""
from __future__ import annotations

import logging
from typing import Optional


def get_logger(name: str = "agentic") -> logging.Logger:
    """Return a configured logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
