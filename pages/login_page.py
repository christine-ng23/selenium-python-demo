# pages/login_page.py
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")

    def login(self, email, password):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
