# pages/registration_form.py
from os import path
from datetime import datetime as dt

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from config.common_config import UPLOAD_DIR, CMD_KEY
from core.base_page import BasePage
from core.react_select import ReactSelect


class RegistrationForm(BasePage):
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    # GENDER_MALE = (By.ID, "gender-radio-1'")
    # GENDER_FEMALE = (By.ID, "gender-radio-2")
    # GENDER_OTHER = (By.ID, "gender-radio-3")
    GENDERS = {"male": (By.CSS_SELECTOR, 'label[for="gender-radio-1"]'),
               "female": (By.CSS_SELECTOR, 'label[for="gender-radio-2"]'),
               "other": (By.CSS_SELECTOR, 'label[for="gender-radio-3"]')}
    MOBILE = (By.ID, "userNumber")
    DATE_OF_BIRTH = (By.ID, "dateOfBirthInput")
    HOBBIES = {"sports": (By.CSS_SELECTOR, 'label[for="hobbies-checkbox-1"]'),
               "reading": (By.CSS_SELECTOR, 'label[for="hobbies-checkbox-2"]'),
               "music": (By.CSS_SELECTOR, 'label[for="hobbies-checkbox-3"]')}
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    SUBMIT = (By.ID, "submit")
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")

    def __init__(self, driver):
        super().__init__(driver)
        self.subject_select = ReactSelect(driver, "#subjectsContainer")
        self.state_select = ReactSelect(driver, "#state")
        self.city_select = ReactSelect(driver, "#city")

    def fill_form(self, data):
        # Remove possible overlay
        self.driver.execute_script("document.getElementById('fixedban')?.remove();")

        self.logger.info("Filling the form...")
        # Filling text field
        text_fields = ["first_name", "last_name", "email", "mobile", "current_address"]
        for field in text_fields:
            self.send_keys(getattr(self, field.upper()), data.get(field, ""), clear=True)
        # Check gender
        if "gender" in data and data["gender"]:
            gender = data["gender"].lower()
            if gender in self.GENDERS:
                self.click(self.GENDERS[gender])
        # Check hobbies
        if "hobbies" in data:
            for hobby in data["hobbies"]:
                hobby = hobby.lower()
                if hobby in self.HOBBIES:
                    self.click(self.HOBBIES[hobby])

        # Filling date of birth
        if "date_of_birth" in data:
            date_of_birth = data["date_of_birth"]
            new_fmt_date_of_birth = dt.strptime(date_of_birth, "%Y/%m/%d").strftime("%d %b %Y")
            date_of_birth_ele = self.send_shortcut(self.DATE_OF_BIRTH, (CMD_KEY, "a"))
            self.reset_keyboard_and_focus()
            self.send_keys(date_of_birth_ele, (new_fmt_date_of_birth, Keys.ENTER))
        # Filling subjects
        if "subjects" in data:
            subjects = data["subjects"]
            self.subject_select.select_all(subjects)
        # Filling state
        if "state" in data:
            state = data["state"]
            self.state_select.select(state)
        # Filling city
        if "city" in data:
            city = data["city"]
            self.city_select.select(city)

        # Upload picture
        if "picture" in data:
            file_path = path.abspath(path.join(UPLOAD_DIR, data["picture"]))
            self.send_keys(self.UPLOAD_PICTURE, file_path)
            self.logger.info(f"Injected the file path: {file_path}")

    def submit(self):
        submit = self.scroll_into_view(self.SUBMIT)
        self.click(submit)

    def is_success_modal_displayed(self):
        try:
            self.find(self.MODAL_TITLE)
            return True
        except:
            return False
