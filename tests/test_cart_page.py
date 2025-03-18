import pytest, time
from pages.cart_page import CartPage
from config.config import CART_PAGE_URL
from locators import CartPageLocators

@pytest.mark.smoke
class TestCartPage:
    """Тесты, связанные с загрузкой страницы корзины и её элементами"""

    def test_cart_page_load_and_elements(self, browser):
        """Проверяет, что страница корзины загружается корректно и все элементы отображаются"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()

        page.wait_for_elements_in_cart() 

        if page.is_product_in_cart():
            product_names = page.get_product_names()
            print("Товары в корзине:", product_names)
            assert product_names, "Товары не отображаются в корзине"
        else:
            cart_table = page.find_element(*CartPageLocators.CART_TABLE)
            assert "empty" in cart_table.text.lower(), "Корзина не пуста"

        assert page.is_element_present(*CartPageLocators.CART_TABLE), "Таблица с товарами не отображается"
        assert page.is_element_present(*CartPageLocators.PLACE_ORDER_BUTTON), "Кнопка оформления заказа не отображается"


@pytest.mark.regression
class TestCartPageActions:
    # @pytest.mark.xfail
    @pytest.mark.repeat(5)
    def test_remove_product(self, browser):
        """Проверяет, что товар можно удалить из корзины и количество товаров уменьшается на 1"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()

        page.wait_for_elements_in_cart()

        initial_product_count = len(page.get_product_names())

        if initial_product_count > 0:
            while page.is_product_in_cart():
                page.wait_for_element(*CartPageLocators.DELETE_BUTTON)
                page.remove_product_from_cart()
                time.sleep(5)

                page.wait_for_elements_in_cart()

                updated_product_count = len(page.get_product_names())

                assert updated_product_count == initial_product_count - 1, \
                    f"Ожидалось, что корзина уменьшится на 1 товар. " \
                    f"Но текущее количество товаров: {updated_product_count}, начальное: {initial_product_count}"

                initial_product_count = updated_product_count

            assert initial_product_count == 0, "Корзина не пуста после удаления всех товаров"
        else:
            print("Корзина пуста, нечего удалять")
            assert not page.is_element_present(*CartPageLocators.DELETE_BUTTON), \
                "Кнопка удаления не должна быть видимой в пустой корзине"

    def test_place_order_button(self, browser):
        """Проверяет, что кнопка 'Оформить заказ' кликабельна"""
        page = CartPage(browser, CART_PAGE_URL)
        page.open()
        assert page.is_element_present(*CartPageLocators.PLACE_ORDER_BUTTON), "Кнопка оформления заказа не кликабельна"
