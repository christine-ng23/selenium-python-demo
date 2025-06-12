# pages/login_page.py
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "userName")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login")
    ERROR_MESSAGE = (By.ID, "name")
    LOGOUT_LINK = (By.XPATH, '//button[contains(text(), "Log out")]')

    def login(self, username, password):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        # Wait and check URL or logout button
        try:
            self.find(self.LOGOUT_LINK)
            return True
        except:
            return False

    def get_error_message(self):
        try:
            return self.find(self.ERROR_MESSAGE).text
        except:
            return ""