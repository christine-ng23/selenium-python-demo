import os
import platform

from selenium.webdriver import Keys

DUMMY_BASE_URL = "https://the-internet.herokuapp.com"
QA_DEMO_URL = "https://demoqa.com"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'test_assets', 'downloads')
UPLOAD_DIR = os.path.join(ROOT_DIR, 'test_assets', 'uploads')
TEST_DATA_DIR = os.path.join(ROOT_DIR, 'test_assets', 'data')
BROWSERS = ["chrome"]
DOWNLOAD_SUPPORTED = ["chrome", "firefox"]
TIMEOUT = 10
IS_HEADLESS = True

CMD_KEY = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
