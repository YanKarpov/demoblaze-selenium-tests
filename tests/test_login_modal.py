import pytest
from components.login_modal import LoginModal
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.smoke
class TestLoginModal:
    """Тесты модального окна логина"""

    def test_login_modal_opens(self, browser):
        """Проверяет, что модальное окно логина открывается"""
        page = LoginModal(browser)
        page.open()  
        assert page.is_modal_open(), "Модальное окно логина не открылось"


    @pytest.mark.parametrize("username, password, expected_success", [
        ("TestYan", "1111", True),
        ("test_user", "wrong_password", False)
    ])
    def test_login(self, browser, username, password, expected_success):
        """Проверяет вход в систему с разными комбинациями логина и пароля"""
        page = LoginModal(browser)
        page.open()
        page.enter_username(username)
        page.enter_password(password)
        page.submit()

        if expected_success:
            page.wait_for_login()
            assert page.is_logged_in(), "Не удалось войти в систему"
        else:
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert_text = alert.text
                alert.accept()
            except TimeoutException:
                assert False, "Ожидался алерт об ошибке входа, но он не появился!"
            
            assert "wrong password" in alert_text.lower(), "Ошибка входа не отображается"
