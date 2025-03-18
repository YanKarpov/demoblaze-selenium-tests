from pages.base_page import BasePage
from config.config import MAIN_URL
from selenium.webdriver.common.by import By

class AuthModal(BasePage):
    """Базовый класс для модальных окон логина и регистрации"""
    
    def __init__(self, browser, open_locator, modal_locator, username_locator, password_locator, submit_locator, close_locator):
        super().__init__(browser, MAIN_URL)
        self.open_locator = open_locator
        self.modal_locator = modal_locator
        self.username_locator = username_locator
        self.password_locator = password_locator
        self.submit_locator = submit_locator
        self.close_locator = close_locator

    def open(self):
        """Открывает модальное окно"""
        super().open()
        self.click(*self.open_locator)
        self.wait_for_element(*self.modal_locator)

    def is_modal_open(self):
        """Проверяет, открылось ли модальное окно"""
        return self.is_element_present(*self.modal_locator)

    def enter_username(self, username):
        self.input_text(*self.username_locator, username)

    def enter_password(self, password):
        self.input_text(*self.password_locator, password)

    def submit(self):
        """Отправляет форму"""
        self.click(*self.submit_locator)

    def close(self):
        """Закрывает модальное окно"""
        self.click(*self.close_locator)
        self.wait_for_element(self.modal_locator, timeout=5)
