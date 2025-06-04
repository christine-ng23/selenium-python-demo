import os

DUMMY_BASE_URL = "https://the-internet.herokuapp.com"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'test_assets', 'downloads')
BROWSERS = ["chrome", "firefox", "safari"]
DOWNLOAD_SUPPORTED = ["chrome", "firefox"]
TIMEOUT = 10
IS_HEADLESS = True
