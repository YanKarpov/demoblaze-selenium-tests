from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CustomAlert:
    def __init__(self, browser, timeout=10):
        self.browser = browser
        self.timeout = timeout

    def wait_for_alert(self):
        """Ожидает появления кастомного алерта."""
        try:
            alert = WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".sweet-alert.showSweetAlert.visible"))
            )
            return alert
        except TimeoutException:
            print("Кастомный алерт не появился")
            return None

    def check_alert_text(self, expected_text):
        """Проверяет, что текст в кастомном алерте соответствует ожидаемому."""
        alert = self.wait_for_alert()
        if alert:
            alert_text = alert.find_element(By.CSS_SELECTOR, "h2").text.strip()
            assert alert_text == expected_text, f"Ожидался текст '{expected_text}', но получен '{alert_text}'"

    def close_alert(self):
        """Закрывает кастомный алерт."""
        try:
            confirm_button = self.browser.find_element(By.CSS_SELECTOR, ".sweet-alert.showSweetAlert.visible .sa-confirm-button-container .confirm")
            if confirm_button:
                confirm_button.click()
        except NoSuchElementException:
            print("Кнопка подтверждения не найдена в кастомном алерте")
