import os

import allure
import pytest
import pytest_check as check

from config.common_config import DUMMY_BASE_URL, QA_DEMO_URL
from core.data_loader import load_json
from pages.iframe_page import IFramePage
# from shared.utils.logger import get_logger
from core.logger import get_logger
from pages.nested_frames_page import NestedFramesPage
from pages.registration_form import RegistrationForm
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


# Load test data
test_data = load_json("form_test_data.json")
# Extract parameters and IDs
test_cases = [(tc["input"], tc["expected_result"]) for tc in test_data ]
test_ids = [tc["id"] + " - " + tc["description"] for tc in test_data]

@pytest.mark.parametrize("input_data,expected", test_cases, ids=test_ids)
def test_form(driver, input_data, expected):
    page = RegistrationForm(driver)
    page.open(f"{QA_DEMO_URL}/automation-practice-form")

    # logger.info("Verifying the page loaded properly")
    # check.is_in("DEMOQA", driver.title, "Page did not load correctly")

    # Soft asserts for visibility
    check.is_true(page.is_displayed(page.FIRST_NAME), "First name field not visible")
    check.is_true(page.is_displayed(page.LAST_NAME), "Last name field not visible")
    check.is_true(page.is_displayed(page.EMAIL), "Email field not visible")
    check.is_true(page.is_displayed(page.MOBILE), "Mobile field not visible")

    # Fill and submit form
    page.fill_form(input_data)
    page.submit()

    # Happy path: modal should appear
    if expected == "Success":
        assert page.is_success_modal_displayed(), f"Modal not shown"
    else:
        assert not page.is_success_modal_displayed(), f"Modal wrongly shown for invalid case"
