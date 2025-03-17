from locators import LoginModalLocators, MainPageLocators
from config.config import MAIN_URL
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginModal(BasePage):
    def __init__(self, browser):
        super().__init__(browser, MAIN_URL)

    def open(self):
        """Открывает главную страницу и открывает модальное окно логина"""
        super().open()
        self.click(*MainPageLocators.LOGIN_BUTTON)
        self.wait_for_element(*LoginModalLocators.MODAL)

    def is_modal_open(self):
        """Проверяет, открылось ли модальное окно"""
        return self.is_element_present(*LoginModalLocators.MODAL)

    def enter_username(self, username):
        """Вводит имя пользователя"""
        self.input_text(*LoginModalLocators.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Вводит пароль"""
        self.input_text(*LoginModalLocators.PASSWORD_INPUT, password)

    def submit(self):
        """Отправляет форму логина"""
        self.click(*LoginModalLocators.LOGIN_BUTTON)

    def close(self):
        """Закрывает модальное окно"""
        self.click(*LoginModalLocators.CLOSE_BUTTON)
        self.wait_for_element(*LoginModalLocators.MODAL, timeout=5)

    def is_logged_in(self):
        """Проверяет, вошел ли пользователь (есть ли кнопка logout)"""
        return self.is_element_present(By.ID, "logout2")

    def wait_for_login(self, timeout=10):
        """Ждет, пока исчезнет 'Log in' и появится 'Log out'"""
        self.wait_for_element(By.ID, "login2", timeout=timeout)
        self.wait_for_element(By.ID, "logout2", timeout=timeout)
