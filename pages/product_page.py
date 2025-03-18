from pages.base_page import BasePage
from locators import ProductPageLocators, CartPageLocators


class ProductPage(BasePage):
    """Методы для работы со страницей товара"""

    def get_product_name(self):
        return self.get_text(*ProductPageLocators.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_text(*ProductPageLocators.PRODUCT_PRICE)

    def get_product_description(self):
        return self.get_text(*ProductPageLocators.PRODUCT_DESCRIPTION)

    def add_to_cart(self):
        """Кликает по кнопке 'Add to Cart'"""
        self.click(*ProductPageLocators.ADD_TO_CART_BUTTON)

    def is_product_image_visible(self):
        """Проверяет, видимо ли изображение товара."""
        return self.is_element_present(*ProductPageLocators.PRODUCT_IMAGE)

    def is_product_title_visible(self):
        """Проверяет, что заголовок товара присутствует на странице."""
        actual_title = self.get_product_name()
        return bool(actual_title)

    def is_product_description_visible(self):
        """Проверяет, видим ли описание товара."""
        return self.is_element_present(*ProductPageLocators.PRODUCT_DESCRIPTION)

    def is_product_price_visible(self):
        """Проверяет, видна ли цена товара."""
        return self.is_element_present(*ProductPageLocators.PRODUCT_PRICE)

    def is_add_to_cart_button_visible(self):
        """Проверяет, видна ли кнопка 'Add to Cart'."""
        return self.is_element_present(*ProductPageLocators.ADD_TO_CART_BUTTON)

    def is_product_added_alert_visible(self):
        """Проверяет, видим ли алерт 'Product added' после добавления товара в корзину."""
        alert = self.is_element_present(*ProductPageLocators.PRODUCT_ADDED_ALERT)
        return alert

    def go_to_cart(self):
        """Переходит в корзину."""
        self.click(*ProductPageLocators.CART_BUTTON)

    def is_product_in_cart(self):
        """Проверяет, есть ли товары в корзине"""
        return self.is_element_present(*CartPageLocators.PRODUCT_NAME_IN_CART)  


 
