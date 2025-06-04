# pages/windows_page.py
from selenium.webdriver.common.by import By

from core.base_page import BasePage


class WindowsPage(BasePage):
    LINK = (By.LINK_TEXT, "Click Here")
    TITLE_HEADER = (By.TAG_NAME, "h3")

    def click_open_new_window_link(self):
        self.click(self.LINK)

    def get_header_text(self):
        return self.find(self.TITLE_HEADER).text
