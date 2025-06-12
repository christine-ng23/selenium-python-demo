import allure
import pytest

from config.common_config import DUMMY_BASE_URL, QA_DEMO_URL
from core.data_loader import load_json
from pages.login_page import LoginPage

# Load JSON once
all_data = load_json("auth_test_data.json")
login_cases = all_data["login"]

test_cases = [
    (tc["id"], tc["input"]["username"], tc["input"]["password"], tc["expected"])
    for tc in login_cases
]
test_ids = [f"{tc['id']} - {tc['description']}" for tc in login_cases[:1]]

@allure.feature('Login')
@pytest.mark.parametrize("case_id, username, password, expected", test_cases, ids=test_ids)
def test_login(driver, case_id, username, password, expected):
    page = LoginPage(driver)
    page.open(f"{QA_DEMO_URL}/login")
    page.login(username, password)

    if expected == "Success":
        assert page.is_login_successful(), "Failed: expected success"
    else:
        assert not page.is_login_successful(), "Failed: expected error"
        if case_id in ["L02", "L03"]:
            assert "Invalid username or password" in page.get_error_message()
