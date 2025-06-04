import os

import allure
import pytest

from config.common_config import DUMMY_BASE_URL
from pages.upload_page import UploadPage
# from shared.utils.logger import get_logger
from core.logger import get_logger

logger = get_logger("TestFileUpload")


@pytest.mark.file_upload
@allure.feature("File Upload")
@allure.tag("Happy")
def test_file_upload(driver):
    filename = 'images.jpeg'
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_assets', 'uploads', 'images.jpeg'))
    driver.get(f'{DUMMY_BASE_URL}/upload')
    logger.info("Navigated to upload page")

    # Initialize page object and perform file upload and submit form
    upload_page = UploadPage(driver)
    upload_page.upload_file(file)
    upload_page.submit()

    # Retrieve uploaded file name from confirmation and assert it matches expected
    uploaded_file = upload_page.get_uploaded_filename()
    logger.info(f"Uploaded file confirmed on UI: {uploaded_file}")
    allure.attach(uploaded_file, name="The Uploaded File", attachment_type=allure.attachment_type.TEXT)

    assert uploaded_file == filename, f"Expected uploaded file to be '{filename}', but got '{uploaded_file}'"
