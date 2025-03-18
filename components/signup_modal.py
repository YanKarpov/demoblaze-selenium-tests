from locators import SignUpModalLocators, MainPageLocators
from components.auth_modal import AuthModal

class SignUpModal(AuthModal):
    def __init__(self, browser):
        super().__init__(
            browser,
            MainPageLocators.SIGNUP_BUTTON,
            SignUpModalLocators.MODAL,
            SignUpModalLocators.USERNAME_INPUT,
            SignUpModalLocators.PASSWORD_INPUT,
            SignUpModalLocators.SIGNUP_BUTTON,
            SignUpModalLocators.CLOSE_BUTTON
        )

    def is_error_message_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке"""
        return self.is_element_present(*SignUpModalLocators.ERROR_MESSAGE)
