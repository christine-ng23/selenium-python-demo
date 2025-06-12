# -----------------------------
# TEST DATA MANAGEMENT
# -----------------------------

# core/data_loader.py
import json
import os

from config.common_config import TEST_DATA_DIR
from core.logger import get_logger

logger = get_logger(__name__)

def load_json(file_name):
    logger.info(f"Load data from {file_name}")
    path = os.path.join(TEST_DATA_DIR, file_name) if not os.path.isabs(file_name) else file_name
    with open(path, 'r') as f:
        return json.load(f)
