import logging
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def open(self):
        """Открывает страницу и применяет неявное ожидание."""
        self.browser.get(self.url)
        self.browser.implicitly_wait(self.timeout)

    def is_element_present(self, how, what):
        """Проверяет наличие элемента на странице."""
        return self._safe_find_element(how, what) is not None

    def find_element(self, how, what):
        """Безопасный поиск элемента."""
        return self._safe_find_element(how, what)

    def find_elements(self, how, what):
        """Находит все элементы по локатору."""
        try:
            return self.browser.find_elements(how, what)
        except NoSuchElementException:
            self._log_error(f"Элементы {what} не найдены!")
            return []

    def _safe_find_element(self, how, what):
        """Пытается найти элемент и возвращает None в случае ошибки."""
        try:
            return self.browser.find_element(how, what)
        except NoSuchElementException:
            self._log_error(f"Элемент {what} не найден!")
            return None

    def is_element_clickable(self, how, what, timeout=10):
        """Проверяет, кликабелен ли элемент."""
        return self._wait_for_element(how, what, timeout, EC.element_to_be_clickable)

    def click(self, how, what, timeout=10):
        """Ожидает и кликает по элементу."""
        try:
            element = self._wait_for_element(how, what, timeout, EC.element_to_be_clickable)
            if element:
                element.click()
        except (ElementClickInterceptedException, TimeoutException) as e:
            self._log_error(f"Не удалось кликнуть по элементу {what}: {str(e)}")

    def get_element_attribute(self, how, what, attribute):
        """Возвращает значение атрибута элемента."""
        element = self.find_element(how, what)
        return element.get_attribute(attribute) if element else None

    def get_text(self, how, what):
        """Получает текст элемента."""
        element = self.find_element(how, what)
        return element.text if element else ""

    def input_text(self, how, what, text, clear_first=True):
        """Вводит текст в поле."""
        element = self.find_element(how, what)
        if element:
            if clear_first:
                element.clear()
            element.send_keys(text)

    def scroll_into_view(self, how, what):
        """Прокручивает страницу до элемента."""
        element = self.find_element(how, what)
        if element:
            self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def hover_over_element(self, how, what):
        """Наводит курсор на элемент."""
        element = self.find_element(how, what)
        if element:
            ActionChains(self.browser).move_to_element(element).perform()

    def wait_for_element(self, how, what, timeout=10):
        """Ожидает появления элемента."""
        return self._wait_for_element(how, what, timeout, EC.presence_of_element_located)

    def _wait_for_element(self, how, what, timeout, condition):
        """Ожидает выполнение условия для элемента."""
        try:
            return WebDriverWait(self.browser, timeout).until(condition((how, what)))
        except TimeoutException:
            self._log_error(f"Элемент {what} не появился на странице")
            return None

    def _log_error(self, message):
        """Логирует ошибку."""
        self.logger.error(message)
