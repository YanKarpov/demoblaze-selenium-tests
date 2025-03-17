import pytest, time
from components.signup_modal import SignUpModal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.data_generator import DataGenerator  


@pytest.mark.smoke
class TestSignUpModal:
    """Тесты модального окна регистрации"""

    def test_signup_modal_opens(self, browser):
        """Проверяет, что модальное окно регистрации открывается"""
        page = SignUpModal(browser)
        page.open()

        assert page.is_modal_open(), "Модальное окно регистрации не открылось"

    @pytest.mark.regression
    def test_valid_registration(self, browser):
        """Проверяет успешную регистрацию нового пользователя"""
        data_gen = DataGenerator()
        timestamp = int(time.time())  
        username = f"{data_gen.generate_username()}_{timestamp}"  
        password = data_gen.generate_password()

        page = SignUpModal(browser)
        page.open()

        page.enter_username(username)
        page.enter_password(password)
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "sign up successful" in alert_text.lower(), "Ошибка: регистрация не удалась"

    @pytest.mark.parametrize("username, password, expected_message", [
        ("existing_user", "password123", "this user already exist."),  # Повторная регистрация
        ("", "", "please fill out"),  # Пустые поля
        pytest.param("short", "123", "password is too short", 
                     marks=pytest.mark.xfail(reason="Система не проверяет длину пароля")),  
        pytest.param("user@name", "password123", "invalid username", 
                     marks=pytest.mark.xfail(reason="Регистрация разрешает спецсимволы в имени пользователя")),  
    ])

    def test_invalid_registration(self, browser, username, password, expected_message):
        """Проверяет различные сценарии неудачной регистрации"""
        page = SignUpModal(browser)
        page.open()

        page.enter_username(username)
        page.enter_password(password)
        page.submit()

        WebDriverWait(browser, 5).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert expected_message in alert_text.lower(), f"Ошибка: ожидалось '{expected_message}', но получено '{alert_text.lower()}'"
