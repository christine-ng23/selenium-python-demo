from selenium.webdriver.common.by import By
from core.base_page import BasePage

class IFramePage(BasePage):
    IFRAME = (By.CSS_SELECTOR, 'iframe[id="mce_0_ifr"]')
    BODY = (By.ID, "tinymce")

    def write_in_iframe(self, text):
        iframe_element = self.find(self.IFRAME)
        self.switch_to_frame(iframe_element)  # Switch to frame using element
        self.type(self.BODY, text, clear=True)
        self.switch_to_default()

    def get_text_from_iframe(self):
        self.switch_to_frame(0)  # Switch to frame using index
        body_text = self.find(self.BODY).text
        self.switch_to_default()
        return body_text

