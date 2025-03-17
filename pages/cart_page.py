from pages.base_page import BasePage
from locators import CartPageLocators
from config.config import CART_PAGE_URL

class CartPage(BasePage):
    """Методы для работы со страницей корзины"""

    def open(self):
        """Открывает страницу корзины"""
        self.browser.get(CART_PAGE_URL)

    def get_product_names(self):
        """Получает список всех товаров в корзине"""
        return self.get_text(*CartPageLocators.PRODUCT_NAME_IN_CART)  # Локатор для названий товаров в корзине

    def get_product_price(self):
        """Получает цену товара в корзине"""
        return self.get_text(*CartPageLocators.PRODUCT_PRICE)  # Локатор для цены товаров (при необходимости)

    def get_total_price(self):
        """Получает общую стоимость товаров в корзине"""
        try:
            total_price_element = self.find_element(*CartPageLocators.TOTAL_PRICE)
            total_price_text = total_price_element.text.strip()
            # Проверка на наличие числового значения в тексте
            if total_price_text and any(char.isdigit() for char in total_price_text):
                return total_price_text
            return None
        except Exception as e:
            print(f"Ошибка при получении общей стоимости: {e}")
            return None


    def remove_product_from_cart(self):
        """Удаляет товар из корзины"""
        self.click(*CartPageLocators.DELETE_BUTTON)  # Локатор для кнопки удаления товара

    def proceed_to_checkout(self):
        """Переходит к оформлению заказа"""
        self.click(*CartPageLocators.PLACE_ORDER_BUTTON)  # Локатор для кнопки оформления заказа

    def is_product_in_cart(self):
        """Проверяет, есть ли товар в корзине"""
        return self.is_element_present(*CartPageLocators.PRODUCT_NAME_IN_CART)  # Проверка наличия товара в корзине

    def is_empty_cart_message_visible(self):
        """Проверяет, что корзина пуста"""
        return self.is_element_present(*CartPageLocators.EMPTY_CART_MESSAGE)  # Локатор для сообщения о пустой корзине
