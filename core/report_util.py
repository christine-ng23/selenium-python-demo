# shared/utils/error_capture.py
import os
import time

import allure


def capture_failure(driver, test_name: str, exception: str, logger):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    screenshot_dir = os.path.join("reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(path)

    # Logging
    logger.error(f"Test failed: {exception}")
    logger.error(f"Screenshot saved at: {path}")

    # Allure attach
    allure.attach.file(path, name=f"{filename}", attachment_type=allure.attachment_type.PNG)
