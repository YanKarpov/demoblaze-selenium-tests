from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.timeout = timeout  

    def open(self):
        """Открывает страницу и применяет неявное ожидание."""
        self.browser.get(self.url)
        self.browser.implicitly_wait(self.timeout)

    def is_element_present(self, how, what):
        """Проверяет наличие элемента на странице."""
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            print(f"Элемент {what} не найден на странице!")
            return False
        return True

    def find_element(self, how, what):
        """Безопасный поиск элемента."""
        try:
            return self.browser.find_element(how, what)
        except NoSuchElementException:
            print(f"Элемент {what} не найден!")
            return None

    def find_elements(self, how, what):
        """Находит все элементы по локатору."""
        try:
            return self.browser.find_elements(how, what)
        except NoSuchElementException:
            print(f"Элементы {what} не найдены!")
            return []

    def is_element_clickable(self, how, what, timeout=10):
        """Проверяет, кликабелен ли элемент"""
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
            return element is not None
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            return False
        
    def click(self, how, what, timeout=10):
        """Ожидает и кликает по элементу."""
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
            element.click()
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            print(f"Не удалось кликнуть по элементу {what}")

    def get_element_attribute(self, how, what, attribute):
        """Возвращает значение атрибута элемента"""
        try:
            element = self.find_element(how, what)
            return element.get_attribute(attribute) if element else None
        except NoSuchElementException:
            print(f"Элемент {what} не найден!")
            return None

    def get_text(self, how, what):
        """Получает текст элемента."""
        try:
            element = self.find_element(how, what)
            return element.text if element else ""
        except NoSuchElementException:
            print(f"Не удалось получить текст элемента {what}")
            return ""

    def input_text(self, how, what, text, clear_first=True):
        """Вводит текст в поле."""
        try:
            element = self.find_element(how, what)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
        except NoSuchElementException:
            print(f"Не удалось ввести текст в элемент {what}")

    def scroll_into_view(self, how, what):
        """Прокручивает страницу до элемента."""
        try:
            element = self.find_element(how, what)
            if element:
                self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        except NoSuchElementException:
            print(f"Не удалось прокрутить к элементу {what}")

    def hover_over_element(self, how, what):
        """Наводит курсор на элемент."""
        try:
            element = self.find_element(how, what)
            if element:
                ActionChains(self.browser).move_to_element(element).perform()
        except NoSuchElementException:
            print(f"Не удалось навести на элемент {what}")

    def wait_for_element(self, how, what, timeout=10):
        """Ожидает появления элемента."""
        try:
            return WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            print(f"Элемент {what} не появился на странице")
            return None
