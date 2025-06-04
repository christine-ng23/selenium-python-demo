# pages/download_page.py
from selenium.webdriver.common.by import By
from core.base_page import BasePage

class DownloadPage(BasePage):
    LINKS = (By.CSS_SELECTOR, "#content a")

    def get_download_links(self):
        return self.driver.find_elements(*self.LINKS)

    def click_link(self, element):
        element.click()
