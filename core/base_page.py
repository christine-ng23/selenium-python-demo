import logging
import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.common_config import TIMEOUT, CMD_KEY
from core.logger import get_logger


class BasePage:
    logger = get_logger(__name__)

    def __init__(self, driver, timeout=TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def _resolve_element(self, target, parent=None):
        """Accepts either a locator tuple or a WebElement and returns the element."""
        if isinstance(target, tuple):
            return self.find(target, parent)
        else:
            return target

    def open(self, url):
        """
        Open a webpage
        :param url: str
        """
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find(self, locator, parent=None):
        """
        Find the element
        :param parent: WebElement
        :param locator: Tuple[str, str]
        :return: WebElement
        """
        self.logger.info(f"Finding element: {locator}")
        context = parent if parent else self.driver
        wait = WebDriverWait(context, self.timeout,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator, parent=None):
        """
        Find all elements
        :param locator: Tuple[str, str]
        :param parent: WebElement
        :return: list[WebElement]
        """
        self.logger.info(f"Finding all elements: {locator}")
        context = parent if parent else self.driver
        wait = WebDriverWait(context, self.timeout,
                             ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, target, parent=None):
        """
        Clicks the element
        :param target: Tuple[str, str] | WebElement
        :param parent: WebElement
        """
        self.logger.info(f"Clicking element: {target}")
        context = parent if parent else self.driver
        return WebDriverWait(context, self.timeout).until(EC.element_to_be_clickable(target)).click()


    def send_keys(self, target, keys, parent=None, clear=False):
        """
        Send keys to an input element
        :param target: Tuple[str, str] | WebElement
        :param keys: str | list[str]
        :param parent: WebElement
        :param clear: boolean: if true, the input will be cleared before entering text
        :return: WebElement
        """
        element = self._resolve_element(target, parent)
        if clear:
            element.clear()
            self.logger.info(f"Cleared element: {target}")

        element.send_keys(keys)
        self.logger.info(f"Sent keys: {keys} into element: {target}")
        return element

    def send_keys_global(self, keys):
        """
        Send global keys without focusing on a specific element.
        Example: send_keys_global(Keys.ENTER)
        :param keys: str | list[str]
        """
        action = ActionChains(self.driver)
        action.send_keys(keys)
        action.perform()
        self.logger.info(f"Sent keys globally: {keys}")

    def send_shortcut(self, target, keys, parent=None):
        """
        Send a shortcut like CTRL+A or CTRL+C to a specific element using ActionChains.
        Example: send_shortcut(locator, (Keys.CONTROL, 'a'))
        :param target: Tuple[str, str] | WebElement
        :param keys: Tuple[str, str]
        :param parent: WebElement
        """
        element = self._resolve_element(target, parent)

        action = ActionChains(self.driver)
        action.click(element)
        for key in keys[:-1]:
            action.key_down(key)
        action.send_keys(keys[-1])
        for key in keys[-1]:
            action.key_up(key)
        action.perform()
        self.logger.info(f"Sent shortcut {keys} into {target}")
        return element

    def drag_and_drop(self, source, target):
        """Drag element from source to target using ActionChains."""
        source_element = self._resolve_element(source)
        target_element = self._resolve_element(target)
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()
        self.logger.info(f"Did drag and drop from {source} to {target}")

    def reset_keyboard_and_focus(self):
        """
        To reset keyboard and focus in these cases:
        Sometimes browser keeps interpreting keyboard input as a shortcut (e.g. CMD+key) after a modifier-based
        action chain.
        Selenium/WebDriver doesn't always reset the keyboard state/focus properly after synthetic modifier key usage.
        """
        self.logger.info(f"Resetting the keyboard and focus")
        ActionBuilder(self.driver).clear_actions()


    def reset_focus_by_js(self, element):
        """Reset the focus by js"""
        self.logger.info(f"Resetting focus by js")
        self.driver.execute_script("arguments[0].blur();", element)
        time.sleep(0.1)
        self.driver.execute_script("arguments[0].focus();", element)
        time.sleep(0.1)

    def copy_paste(self, source, target):
        """Copy from source and paste into target using ActionChains."""
        source_element = self._resolve_element(source)
        target_element = self._resolve_element(target)

        actions = ActionChains(self.driver)
        actions.click(source_element)
        actions.key_down(CMD_KEY).send_keys('a').key_up(CMD_KEY).perform()
        actions.key_down(CMD_KEY).send_keys('c').key_up(CMD_KEY).perform()
        actions.click(target_element)
        actions.key_down(CMD_KEY).send_keys('v').key_up(CMD_KEY).perform()
        self.logger.info(f"Did copy paste from {source} to {target}")

    def is_displayed(self, locator, parent=None):
        """
        Check if an element displayed in webpage.
        :param locator: Tuple[str, str]
        :param parent: WebElement
        :return: WebElement
        """
        context = parent if parent else self.driver
        self.logger.info(f"Checking if {locator} displayed")
        return WebDriverWait(context, self.timeout).until(EC.visibility_of_element_located(locator)).is_displayed()

    def switch_to_frame(self, frame):
        """
        Switch focus to a frame.
        :param frame: str | int | WebElement: name, id, index or web element representing the iframe
        """
        self.driver.switch_to.frame(frame)
        self.logger.info(f"Switched to frame {frame}")

    def switch_to_default(self):
        """ Switch focus to the default frame."""
        self.driver.switch_to.default_content()
        self.logger.info(f"Switched to default")

    def switch_to_window(self, index=-1):
        """
        Switch focus to a window
        :param index: The name or window handle. Default value is -1 representing the last window in the handlers.
        """
        self.driver.switch_to.window(self.driver.window_handles[index])
        self.logger.info(f"Switched to window with index {index}")

    def wait_for_new_window(self, old_handles):
        """
        Wait for the window handles of all windows within the current session to increase
        :param old_handles: List[str]
        """
        self.logger.info("Waiting for new window...")
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(d.window_handles) > len(old_handles)
        )

    def switch_to_new_window(self, old_handles):
        """
        Switch to the new window
        :param old_handles: List[str]
        """
        self.wait_for_new_window(old_handles)
        new_handles = set(self.driver.window_handles) - set(old_handles)
        new_window = new_handles.pop()
        self.driver.switch_to.window(new_window)
        self.logger.info(f"Switched to new window: {new_window}")

    def find_element_in_shadow_dom(self, shadow_host_locator: str, inner_locator: str):
        """
        Find an element in shadow DOM
        :param shadow_host_locator: List[str]
        :param inner_locator: List[str]
        :return: WebElement
        """
        self.logger.info(f"Finding element in shadow DOM with shadow host {shadow_host_locator} and inner locator "
                         f"{inner_locator}")
        shadow_host = self.driver.find_element(shadow_host_locator)
        shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
        return shadow_root.find_element(inner_locator)

    def scroll_into_view(self, target):
        self.logger.info(f"Scroll into view {target}")
        element = self._resolve_element(target)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element