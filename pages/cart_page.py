from pages.base_page import BasePage
from locators import CartPageLocators
from config.config import CART_PAGE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CartPage(BasePage):
    """Методы для работы со страницей корзины"""

    def open(self):
        """Открывает страницу корзины"""
        self.browser.get(CART_PAGE_URL)

    def wait_for_elements_in_cart(self):
        """Ждёт появления всех элементов корзины на странице"""
        self.wait_for_element(*CartPageLocators.PRODUCT_NAME_IN_CART)

    def get_product_names(self):
        """Получает список всех товаров в корзине, ожидая их появления"""
        self.wait_for_element(*CartPageLocators.PRODUCT_NAME_IN_CART)
        product_elements = self.find_elements(*CartPageLocators.PRODUCT_NAME_IN_CART)
        return [element.text for element in product_elements]

    def get_product_price(self):
        """Получает цену товара в корзине"""
        return self.get_text(*CartPageLocators.PRODUCT_PRICE)

    def get_total_price(self):
        """Получает общую стоимость товаров в корзине"""
        total_price_element = self.find_element(*CartPageLocators.TOTAL_PRICE)
        if total_price_element:
            total_price_text = total_price_element.text.strip()
            if total_price_text and any(char.isdigit() for char in total_price_text):
                return total_price_text
        return None

    def remove_product_from_cart(self):
        """Удаляет товар из корзины"""
        self.click(*CartPageLocators.DELETE_BUTTON)

    def proceed_to_checkout(self):
        """Переходит к оформлению заказа"""
        self.click(*CartPageLocators.PLACE_ORDER_BUTTON)

    def is_product_in_cart(self):
        """Проверяет, есть ли товар в корзине"""
        return self.is_element_present(*CartPageLocators.PRODUCT_NAME_IN_CART)

    def wait_for_element_to_be_clickable(self, how, what, timeout=10):
        """Ожидает, пока элемент не станет кликабельным."""
        if not self.is_element_present(how, what):
            self._log_error(f"Элемент {what} не найден на странице.")
            return False

        try:
            WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            self._log_error(f"Элемент {what} не стал кликабельным за {timeout} секунд.")
            return False
        return True
