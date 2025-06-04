# pages/upload_page.py
from selenium.webdriver.common.by import By
from core.base_page import BasePage
from core.logger import get_logger

logger = get_logger("TestFileUpload")

class UploadPage(BasePage):

    FILE_UPLOAD = (By.ID, "file-upload")
    SUBMIT_BTN = (By.ID, "file-submit")
    UPLOADED_FILE = (By.ID, "uploaded-files")

    def upload_file(self, file_path):
        self.type(self.FILE_UPLOAD, file_path)
        logger.info(f"Injected the file path into the form: {file_path}")

    def submit(self):
        self.click(self.SUBMIT_BTN)
        logger.info("Submitted the form")

    def get_uploaded_filename(self):
        return self.find(self.UPLOADED_FILE).text
