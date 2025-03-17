import pytest
from components.login_modal import LoginModal
import time
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginModalLocators


@pytest.mark.smoke
class TestLoginModal:
    """Тесты модального окна логина"""

    def test_login_modal_opens(self, browser):
        """Проверяет, что модальное окно логина открывается"""
        page = LoginModal(browser)
        page.open()  
        assert page.is_modal_open(), "Модальное окно логина не открылось"

    def test_valid_login(self, browser):
        """Проверяет успешный вход в систему"""
        page = LoginModal(browser)
        page.open()
        page.enter_username("TestYan")
        page.enter_password("1111")
        page.submit()

        # page.wait_for_login()
        time.sleep(3)


        assert page.is_logged_in(), "Не удалось войти в систему"





    def test_invalid_login(self, browser):
        """Проверяет, что алерт появляется при неправильном пароле"""
        page = LoginModal(browser)
        page.open()

        # Ждем, когда поле username станет кликабельным
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(LoginModalLocators.USERNAME_INPUT)
        ).send_keys("test_user")

        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(LoginModalLocators.PASSWORD_INPUT)
        ).send_keys("wrong_password")

        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(LoginModalLocators.LOGIN_BUTTON)
        ).click()

        # Ждем появления алерта
        WebDriverWait(browser, 5).until(EC.alert_is_present())

        try:
            alert = browser.switch_to.alert
            alert_text = alert.text
            alert.accept()  # Закрывает алерт
        except NoAlertPresentException:
            alert_text = ""

        assert "wrong password" in alert_text.lower(), "Ошибка входа не отображается"


