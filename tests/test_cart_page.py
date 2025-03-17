import pytest
from pages.cart_page import CartPage
from config.config import CART_PAGE_URL
from locators import CartPageLocators
from selenium.webdriver.common.by import By


@pytest.mark.smoke
class TestCartPage:
    """Тесты, связанные с загрузкой страницы корзины и её элементами"""

    def test_cart_page_load_and_elements(self, browser):
        """Проверяет, что страница корзины загружается корректно и все элементы отображаются"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()

        # Проверка состояния корзины
        if page.is_product_in_cart():
            assert page.get_product_names(), "Товары не отображаются в корзине"
        else:
            cart_table = page.find_element(*CartPageLocators.CART_TABLE)
            rows = cart_table.find_elements(By.TAG_NAME, "tr")
            assert len(rows) == 0, "Корзина не пуста, хотя должна быть пустой"

        # Проверка элементов
        assert page.is_element_present(*CartPageLocators.CART_TABLE), "Таблица с товарами не отображается"
        assert page.is_element_present(*CartPageLocators.PLACE_ORDER_BUTTON), "Кнопка оформления заказа не отображается"


@pytest.mark.regression
class TestCartPageActions:
    """Тесты, связанные с действиями на странице корзины (кнопки)"""

    def test_remove_product(self, browser):
        """Проверяет, что товар можно удалить из корзины"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()

        if page.is_product_in_cart():
            # Ждем, пока кнопка удаления станет видимой и кликаем
            page.wait_for_element_to_be_clickable(*CartPageLocators.DELETE_BUTTON)
            page.click(*CartPageLocators.DELETE_BUTTON)

            # Проверяем, что товар был удален
            assert not page.is_product_in_cart(), "Товар не был удален из корзины"
        else:
            print("Корзина пуста, нечего удалять")
            # Дополнительно проверяем, что кнопка удаления не присутствует, если корзина пуста
            assert not page.is_element_present(*CartPageLocators.DELETE_BUTTON), "Кнопка удаления не должна быть видимой в пустой корзине"

    def test_place_order_button(self, browser):
        """Проверяет, что кнопка 'Оформить заказ' кликабельна"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()
        assert page.is_element_present(*CartPageLocators.PLACE_ORDER_BUTTON), "Кнопка оформления заказа не кликабельна"
