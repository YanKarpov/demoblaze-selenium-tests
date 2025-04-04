from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger

class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.timeout = timeout
        self.logger = logger

    def open(self):
        """Открывает страницу и применяет неявное ожидание."""
        self.logger.info(f"Открытие страницы: {self.url}")
        self.browser.get(self.url)
        self.browser.implicitly_wait(self.timeout)

    def is_element_present(self, how, what):
        """Проверяет наличие элемента на странице."""
        element = self._safe_find_element(how, what)
        if element:
            self.logger.info(f"Элемент {what} присутствует на странице.")
        return element is not None

    def find_element(self, how, what):
        """Безопасный поиск элемента."""
        element = self._safe_find_element(how, what)
        if element:
            self.logger.info(f"Найден элемент {what}.")
        return element

    def find_elements(self, how, what):
        """Находит все элементы по локатору."""
        try:
            elements = self.browser.find_elements(how, what)
            count = len(elements)
            if count > 0:
                self.logger.info(f"Найдено {count} элементов {what}.")
            else:
                self._log_error(f"Элементы {what} не найдены!")
            return elements
        except NoSuchElementException:
            self._log_error(f"Ошибка поиска элементов {what}!")
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
        element = self._wait_for_element(how, what, timeout, EC.element_to_be_clickable)
        if element:
            self.logger.info(f"Элемент {what} кликабелен.")
        return element

    def click(self, how, what, timeout=10):
        """Ожидает и кликает по элементу."""
        try:
            element = self._wait_for_element(how, what, timeout, EC.element_to_be_clickable)
            if element:
                element.click()
                self.logger.info(f"Клик по элементу {what} выполнен успешно.")
        except (ElementClickInterceptedException, TimeoutException) as e:
            self._log_error(f"Не удалось кликнуть по элементу {what}: {str(e)}")

    def get_element_attribute(self, how, what, attribute):
        """Возвращает значение атрибута элемента."""
        element = self.find_element(how, what)
        if element:
            value = element.get_attribute(attribute)
            self.logger.info(f"Атрибут {attribute} у элемента {what}: {value}")
            return value
        return None

    def get_text(self, how, what):
        """Получает текст элемента."""
        element = self.find_element(how, what)
        if element:
            text = element.text
            self.logger.info(f"Текст элемента {what}: {text}")
            return text
        return ""

    def input_text(self, how, what, text, clear_first=True):
        """Вводит текст в поле."""
        element = self.find_element(how, what)
        if element:
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Введен текст в элемент {what}: {text}")

    def wait_for_element(self, how, what, timeout=10):
        """Ожидает появления элемента."""
        return self._wait_for_element(how, what, timeout, EC.presence_of_element_located)

    def _wait_for_element(self, how, what, timeout, condition):
        """Ожидает выполнение условия для элемента."""
        try:
            element = WebDriverWait(self.browser, timeout).until(condition((how, what)))
            self.logger.info(f"Элемент {what} успешно найден с условием {condition.__name__}.")
            return element
        except TimeoutException:
            self._log_error(f"Элемент {what} не появился на странице в течение {timeout} секунд")
            return None

    def _log_error(self, message):
        """Логирует ошибку."""
        self.logger.error(f"[ERROR] {message}")
