import os

import allure
import pytest
import requests
from selenium.webdriver.support.ui import WebDriverWait

from config.common_config import DUMMY_BASE_URL
from pages.download_page import DownloadPage
# from shared.utils.logger import get_logger
from core.logger import get_logger

logger = get_logger("TestFileDownload")

@allure.feature("File Download")
@allure.tag("Happy")
@pytest.mark.download
@pytest.mark.only_on("chrome", "firefox")
def test_file_download(driver_with_download_dir):
    driver, download_dir = driver_with_download_dir
    # Navigate to the download page
    driver.get(f"{DUMMY_BASE_URL}/download")
    logger.info("Navigated to download page")

    download_page = DownloadPage(driver)
    links = download_page.get_download_links()
    assert len(links) >= 3, "Not enough files to download. Expected at least 3."

    downloaded_files = []
    for i in range(1, 3):
        file_name = links[i].text
        file_path = os.path.join(download_dir, file_name)
        download_page.click(links[i])
        logger.info(f"Clicked to download: {file_name}")
        downloaded_files.append(file_path)

    wait = WebDriverWait(driver, 10, poll_frequency=1)
    for file_path in downloaded_files:
        wait.until(lambda x: os.path.exists(file_path))
        assert os.path.exists(file_path), f"Expected downloaded file at: {file_path}"
        logger.info(f"Verified file exists: {file_path}")
        allure.attach(file_path, name="Downloaded File", attachment_type=allure.attachment_type.TEXT)


@allure.feature("File Download")
@allure.tag("Happy")
@pytest.mark.download
def test_file_download_by_request(driver):
    # Navigate to download page
    driver.get(f"{DUMMY_BASE_URL}/download")
    logger.info("Navigated to download page")

    download_page = DownloadPage(driver)
    links = download_page.get_download_links()
    assert len(links) >= 1, "There is no files to download."

    file_name = links[0].text
    file_url = links[0].get_attribute("href")
    if not DUMMY_BASE_URL in file_url:
        file_url = f"{DUMMY_BASE_URL}/{file_url}"

    # Download the file directly via HTTP
    file_response = requests.get(file_url)
    logger.info(f"Sent request to {file_url}.")
    assert file_response.status_code == 200, f"Failed to download {file_name}"
    assert file_response.content, "Downloaded file is empty"

    # Check if it's a text file, PDF, etc.
    logger.info(f"Verified: downloaded file {file_name} ({len(file_response.content)} bytes)")
