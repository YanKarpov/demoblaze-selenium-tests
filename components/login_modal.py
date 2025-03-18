from selenium.webdriver.common.by import By
from locators import LoginModalLocators, MainPageLocators
from components.auth_modal import AuthModal

class LoginModal(AuthModal):
    def __init__(self, browser):
        super().__init__(
            browser,
            MainPageLocators.LOGIN_BUTTON,
            LoginModalLocators.MODAL,
            LoginModalLocators.USERNAME_INPUT,
            LoginModalLocators.PASSWORD_INPUT,
            LoginModalLocators.LOGIN_BUTTON,
            LoginModalLocators.CLOSE_BUTTON
        )

    def wait_for_login(self, timeout=10):
        """Ждет, пока исчезнет 'Log in' и появится 'Log out'"""
        self.wait_for_element(By.ID, "login2", timeout=timeout)
        self.wait_for_element(By.ID, "logout2", timeout=timeout)

    def is_logged_in(self):
        """Проверяет, вошел ли пользователь (есть ли кнопка logout)"""
        return self.is_element_present(By.ID, "logout2")
