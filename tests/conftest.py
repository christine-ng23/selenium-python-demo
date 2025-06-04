import os
import uuid

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from config.common_config import DOWNLOAD_DIR, BROWSERS, IS_HEADLESS, DOWNLOAD_SUPPORTED
from core.logger import get_logger
from core.report_util import capture_failure

logger = get_logger(__name__)


@pytest.fixture(params=BROWSERS)
def driver(request):
    browser = request.param
    if browser == "chrome":
        options = ChromeOptions()
        if IS_HEADLESS:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if IS_HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    elif browser == "safari":
        driver = webdriver.Safari()  # No headless mode or option config

    elif browser == "edge":
        options = EdgeOptions()
        if IS_HEADLESS:
            options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    logger.info(f"Initialized {browser}.")
    yield driver
    driver.quit()
    logger.info(f"Quited {browser}.")



@pytest.fixture(params=BROWSERS)
def driver_with_download_dir(request):
    browser = request.param
    download_subdir = str(uuid.uuid4())
    download_dir = os.path.join(DOWNLOAD_DIR, download_subdir)
    os.makedirs(download_dir, exist_ok=True)

    if browser == "chrome":
        options = ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        if IS_HEADLESS:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.set_preference("browser.download.dir", download_dir)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        if IS_HEADLESS:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

    elif browser == "safari":
        # Safari doesn't support setting download dir programmatically. Users must configure it manually.
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    logger.info(f"Initialized {browser} with download directory {download_dir}.")
    yield driver, download_dir
    driver.quit()


def pytest_sessionstart(session):
    logger.info("Starting test session")


def pytest_sessionfinish(session, exitstatus):
    logger.info(f"Finished test session with exit code {exitstatus}")


def pytest_runtest_setup(item):
    logger.info(f"Setting up for: {item.name}")
    # Allure report - Assign the test's feature label
    if "test_web_elements.py" in str(item.fspath):
        allure.dynamic.feature("Web Elements")

    browser = None
    if hasattr(item, "callspec"):
        params = item.callspec.params
        for key, value in item.callspec.params.items():
            if key in ["driver", "driver_with_download_dir"]:
                browser = value
                break

    # # Solution 1: Skip if browser is not supported and the tests marked 'download'
    # if "download" in item.keywords and browser and browser not in DOWNLOAD_SUPPORTED:
    #     pytest.skip("Download tests are not supported on Safari")

    # Solution 2: Using custom markers
    only_on = item.get_closest_marker("only_on")
    skip_on = item.get_closest_marker("skip_on")

    if only_on and browser not in only_on.args:
        logger.info(f"Dynamic skip for {browser}")
        pytest.skip(f"Only runs on {only_on.args}")
    if skip_on and browser in skip_on.args:
        pytest.skip(f"Skipped own {browser}")
        logger.info(f"Dynamic skip for {browser}")


def pytest_runtest_teardown(item, nextitem):
    pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    logger.info(f"pytest_runtest_makereport for {item.name} when {report.when}: {report.outcome},{report.failed}")
    # Capture screenshot when the test failed
    if report.when == "call":
        if report.failed:
            fixtures = item.funcargs
            drivers = [fixtures[fixture] for fixture in fixtures if "driver" in fixture]
            if drivers:
                test_name = item.name
                exception_info = call.excinfo  # this is a _pytest._code.ExceptionInfo object
                exception_str = str(exception_info.value)
                capture_failure(drivers[0], test_name, exception_str, logger)


def pytest_exception_interact(call, report):
    pass

@pytest.fixture(scope="class")
def class_fix():
    logger.info("class_fix")
    yield
    logger.info("class_fix end")


@pytest.fixture(scope="module")
def module_fix():
    logger.info("module_fix")
    yield
    logger.info("module_fix end")


@pytest.fixture(scope="package")
def package_fix():
    logger.info("package_fix")
    yield
    logger.info("package_fix end")


@pytest.fixture(scope="session")
def session_fix():
    logger.info("session_fix")
    yield
    logger.info("session_fix end")


