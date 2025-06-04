import allure

from config.common_config import DUMMY_BASE_URL
from core.user_data_loader import load_user_data
from pages.home_page import HomePage
from pages.login_page import LoginPage


@allure.feature('Login')
@allure.story('Valid Login')
def test_valid_login(driver):
    users = load_user_data()
    user = users["valid_user"]
    driver.get(f"{DUMMY_BASE_URL}/login")
    login_page = LoginPage(driver)
    login_page.login(user["email"], user["password"])
    home_page = HomePage(driver)
    assert home_page.is_loaded()
