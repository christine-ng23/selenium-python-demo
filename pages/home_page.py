# pages/home_page.py
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class HomePage(BasePage):
    GREETING = (By.CSS_SELECTOR, "h1.welcome")

    def is_loaded(self):
        return self.is_displayed(self.GREETING)

