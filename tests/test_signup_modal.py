import pytest
from components.signup_modal import SignUpModal
from locators import SignUpModalLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


@pytest.mark.smoke
class TestSignUpModal:
    """Тесты модального окна регистрации"""

    def test_signup_modal_opens(self, browser):
        """Проверяет, что модальное окно регистрации открывается"""
        page = SignUpModal(browser)
        page.open()

        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located(SignUpModalLocators.MODAL)
        )
        assert page.is_modal_open(), "Модальное окно регистрации не открылось"

    def test_valid_registration(self, browser):
        """Проверяет успешную регистрацию нового пользователя"""
        page = SignUpModal(browser)
        page.open()

        username = "new_user_123"
        password = "securePassword1!"
        page.enter_username(username)
        page.enter_password(password)
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "signup successful" in alert_text.lower(), "Ошибка: регистрация не удалась"

    def test_existing_user_registration(self, browser):
        """Проверяет, что появляется сообщение об ошибке при попытке зарегистрировать уже существующего пользователя"""
        page = SignUpModal(browser)
        page.open()

        page.enter_username("existing_user")
        page.enter_password("password123")
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "user already exists" in alert_text.lower(), "Ошибка: не появилось сообщение о существующем пользователе"

    def test_empty_fields(self, browser):
        """Проверяет, что появляется ошибка при пустых полях"""
        page = SignUpModal(browser)
        page.open()
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "please fill out" in alert_text.lower(), "Ошибка: нет предупреждения о незаполненных полях"

    def test_invalid_email_format(self, browser):
        """Проверяет, что появляется ошибка при неправильном формате email"""
        page = SignUpModal(browser)
        page.open()

        page.enter_username("invalid_email")
        page.enter_password("password123")
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "invalid email" in alert_text.lower(), "Ошибка: система не проверяет формат email"
