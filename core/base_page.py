import logging
import os
import time

import allure
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.common_config import TIMEOUT
from core.logger import get_logger


class BasePage:
    logger = get_logger(__name__)

    def __init__(self, driver, timeout=TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def _screenshot_on_fail(self, action: str):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{action}_{timestamp}.png"
        path = os.path.join("reports", "screenshots", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
        allure.attach.file(path, name=f"Screenshot - {action}", attachment_type=allure.attachment_type.PNG)
        self.logger.error(f"📸 Screenshot saved at: {path}")

    def open(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find(self, locator):
        self.logger.info(f"Finding by locator: {locator}")
        wait = WebDriverWait(self.driver, self.timeout,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        self.logger.info(f"Finding all by locator: {locator}")
        wait = WebDriverWait(self.driver, self.timeout,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.logger.info(f"Clicking element: {locator}")
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type(self, locator, text, clear=False):
        element = self.find(locator)
        if clear:
            element.clear()
            self.logger.info(f"Clear")

        element.send_keys(text)
        self.logger.info(f"Type text: {text}")

    def is_displayed(self, locator):
        self.logger.info(f"Checking if {locator} displayed")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).is_displayed()

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)
        self.logger.info(f"Switch to frame {frame}")

    def switch_to_default(self):
        self.logger.info(f"Switch to default")
        self.driver.switch_to.default_content()

    def switch_to_window(self, index=-1):
        self.logger.info(f"Switching to window with index {index}")
        self.driver.switch_to.window(self.driver.window_handles[index])

    def wait_for_new_window(self, old_handles):
        self.logger.info("Waiting for new window...")
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(d.window_handles) > len(old_handles)
        )

    def switch_to_new_window(self, old_handles):
        self.wait_for_new_window(old_handles)
        new_handles = set(self.driver.window_handles) - set(old_handles)
        new_window = new_handles.pop()
        self.driver.switch_to.window(new_window)
        self.logger.info(f"Switched to new window: {new_window}")

    def get_text(self, locator, description=""):
        with allure.step(f"Get text from: {description or locator}"):
            try:
                self.logger.info(f"Getting text from {locator}")
                return self.find(locator, description).text
            except Exception as e:
                self._screenshot_on_fail(f"gettext_{description or locator}")
                self.logger.error(f"Failed to get text from {locator}: {e}")
                raise

    def find_element_in_shadow_dom(self, shadow_host_locator: str, inner_locator: str):
        shadow_host = self.driver.find_element(shadow_host_locator)
        shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
        return shadow_root.find_element(inner_locator)
