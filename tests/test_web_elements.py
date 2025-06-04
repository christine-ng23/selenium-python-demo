import os

import allure
import pytest

from config.common_config import DUMMY_BASE_URL
from pages.iframe_page import IFramePage
# from shared.utils.logger import get_logger
from core.logger import get_logger
from pages.nested_frames_page import NestedFramesPage
from pages.windows_page import WindowsPage

logger = get_logger(__name__)

@pytest.mark.skip(reason="This test is skipped unconditionally")
def test_iframe(driver):
    driver.get(f"{DUMMY_BASE_URL}/iframe")
    page = IFramePage(driver)

    page.write_in_iframe("Hello Selenium")
    text = page.get_text_from_iframe()
    logger.info(f"iFrame Text: {text}")

    assert "Hello Selenium" in text


@pytest.mark.skip(reason="This test is skipped unconditionally")
def test_nested_frames(driver, class_fix, module_fix, package_fix, session_fix):
    driver.get(f"{DUMMY_BASE_URL}/nested_frames")

    page = NestedFramesPage(driver)

    left = page.get_left_frame_text()
    logger.info(f"Left Frame Text: {left}")

    middle = page.get_middle_frame_text()
    logger.info(f"Middle Frame Text: {middle}")

    bottom = page.get_bottom_frame_text()
    logger.info(f"Bottom Frame Text: {bottom}")

    assert left == "LEFT"
    assert middle == "MIDDLE"
    assert bottom == "BOTTOM"


def test_handle_multiple_windows(driver):
    page = WindowsPage(driver)
    page.open(f"{DUMMY_BASE_URL}/windows")

    # Store the current window
    original_window = driver.current_window_handle
    original_handles = driver.window_handles

    # Click link to open new window
    page.click_open_new_window_link()
    logger.info("Clicked link to open new window")

    # Wait and switch to the new window
    page.switch_to_new_window(original_handles)
    logger.info("Switched to the new browser window")

    # Assert new window content
    assert page.get_header_text() == "New Window"
    logger.info("Verified header text in new window")

    # Close new window and return to original
    driver.close()
    driver.switch_to.window(original_window)
    logger.info("Closed new window and returned to original")

