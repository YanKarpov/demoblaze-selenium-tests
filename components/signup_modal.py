from locators import SignUpModalLocators, MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import BASE_URL
from selenium.webdriver.common.by import By


class SignUpModal:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        """Открывает модальное окно регистрации, кликая по кнопке на главной странице"""
        self.driver.get(BASE_URL)
        self.driver.find_element(*MainPageLocators.SIGNUP_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(SignUpModalLocators.MODAL)
        )

    def is_modal_open(self):
        """Проверяет, открылось ли модальное окно"""
        return bool(self.driver.find_elements(*SignUpModalLocators.MODAL))

    def enter_username(self, username):
        self.driver.find_element(*SignUpModalLocators.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*SignUpModalLocators.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        """Нажимает кнопку регистрации"""
        self.driver.find_element(*SignUpModalLocators.SIGNUP_BUTTON).click()

    def close(self):
        """Закрывает модальное окно"""
        self.driver.find_element(*SignUpModalLocators.CLOSE_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(SignUpModalLocators.MODAL)
        )

    def is_error_message_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке"""
        return bool(self.driver.find_elements(*SignUpModalLocators.ERROR_MESSAGE))
