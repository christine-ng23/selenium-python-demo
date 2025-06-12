from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from core.base_page import BasePage


class ReactSelect(BasePage):
    # OPTION = (By.XPATH, "//*[contains(@class,'_option') and normalize-space(text())='{option_text}']")
    OPTION = (By.XPATH, "//div[contains(@class,'_option') and contains(text(),'{option_text}')]")

    def __init__(self, driver, root_selector, is_single=True):
        """
        :param root_selector: str: CSS selector that scopes the control container
        """
        super().__init__(driver)
        self.root_selector = root_selector
        self.control = (By.CSS_SELECTOR, f"{root_selector} [class*=\"control\"]")
        self.input = (By.CSS_SELECTOR, f"{root_selector} input")
        self.hidden_input = (By.CSS_SELECTOR, f"{root_selector} input[name]")
        self.is_single = is_single

    def select_all(self, options):
        """
        :param options: list[str]
        """
        self.logger.info(f"Selecting option {options}")
        for option_text in options:
            self.select(option_text)

    def select(self, option_text):
        """
        :param option_text: str
        """
        # Scroll and click safely
        control = self.scroll_into_view(self.control)
        # Click control to activate input
        self.click(control)
        # Type option text
        self.send_keys(self.input, (option_text, Keys.TAB))
        self.reset_keyboard_and_focus()
        # # Wait and click the matching option
        # self.send_keys(self.input, option_text)
        # self.click((self.OPTION[0], self.OPTION[1].format(option_text=option_text)))
        self.logger.info(f"Selected option {option_text}")

    def get_hidden_input_value(self):
        """Return the hidden input value as str for single select and list[str] for multi select"""
        if self.is_single:
            res = self.find(self.hidden_input).get_attribute("value")
            self.logger.info(f"Get hidden input value: {res}")
        else:
            hidden_inputs = self.find_all(self.hidden_input)
            res = {inp.get_attribute("value") for inp in hidden_inputs}
            self.logger.info(f"Get hidden input values: {res}")
        return res
