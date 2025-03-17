from pages.base_page import BasePage
from locators import SignUpModalLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.config import BASE_URL


class SignUpModal(BasePage):
    def __init__(self, browser):
        super().__init__(browser, BASE_URL)

    def open(self):
        """Открывает модальное окно регистрации"""
        self.click(By.ID, "signin2")  
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(SignUpModalLocators.MODAL)
        )

    def enter_username(self, username):
        self.input_text(*SignUpModalLocators.USERNAME_INPUT, text=username)

    def enter_password(self, password):
        self.input_text(*SignUpModalLocators.PASSWORD_INPUT, text=password)

    def submit(self):
        self.click(*SignUpModalLocators.SIGNUP_BUTTON)

    def close(self):
        self.click(*SignUpModalLocators.CLOSE_BUTTON)

    def is_modal_open(self):
        """Проверяет, открыто ли модальное окно"""
        return self.is_element_visible(*SignUpModalLocators.MODAL)
