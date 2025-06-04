# pages/home_page.py
from selenium.webdriver.common.by import By

from tests.conftest import driver
from core.base_page import BasePage

class NestedFramesPage(BasePage):
    LEFT_FRAME_BODY = (By.TAG_NAME, "body")
    MIDDLE_FRAME_CONTENT = (By.ID, "content")
    BOTTOM_FRAME_BODY = (By.TAG_NAME, "body")

    def get_left_frame_text(self):
        self.switch_to_frame("frame-top")
        self.switch_to_frame("frame-left")
        body_text = self.find(self.LEFT_FRAME_BODY).text
        self.switch_to_default()
        return body_text

    def get_middle_frame_text(self):
        self.switch_to_frame(0)  # frame-top
        self.switch_to_frame("frame-middle")
        content_text = self.find(self.MIDDLE_FRAME_CONTENT).text
        self.switch_to_default()
        return content_text

    def get_bottom_frame_text(self):
        self.switch_to_frame(1)  # frame-bottom
        body_text = self.find(self.BOTTOM_FRAME_BODY).text
        self.switch_to_default()
        return body_text


