# -----------------------------
# CORE LIBRARIES
# -----------------------------

# core/logger.py
import inspect
import logging
import sys

LOG_FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
LOG_LEVEL = logging.INFO  # or INFO for less detail

def get_caller_info():
    frame = inspect.currentframe().f_back  # Go back one frame (to the caller)
    info = inspect.getframeinfo(frame)

    # Get class name if available
    cls = None
    if 'self' in frame.f_locals:
        cls = type(frame.f_locals['self']).__name__

    return {
        'filename': info.filename,
        'function': info.function,
        'lineno': info.lineno,
        'class': cls
    }

def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        # Ensure messages bubble up to root (so Pytest/Allure captures them)
        logger.propagate = True

        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
