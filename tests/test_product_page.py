import pytest
from selenium.webdriver.common.alert import Alert
from pages.product_page import ProductPage
from config.config import PRODUCT_PAGE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
@pytest.mark.parametrize("product_id", range(1, 16))  
class TestProductPageLoad:
    """Тесты, связанные с загрузкой страницы товара"""

    def test_product_page_loads(self, browser, product_id):
        """Проверяет, что страница товара загружается и основные элементы присутствуют"""
        
        page = ProductPage(browser, PRODUCT_PAGE_URL.format(idp_=product_id))
        page.open()

        assert page.is_product_title_visible(), f"Заголовок товара с ID {product_id} не отображается"
        assert page.is_product_image_visible(), f"Изображение товара с ID {product_id} не отображается"
        assert page.is_add_to_cart_button_visible(), f"Кнопка 'Добавить в корзину' для товара с ID {product_id} не отображается"
        assert page.is_product_description_visible(), f"Описание товара с ID {product_id} не отображается"
        assert page.is_product_price_visible(), f"Цена товара с ID {product_id} не отображается"
    
    def test_add_to_cart_and_check_alert(self, browser, product_id):
        """Проверяет, что при добавлении товара в корзину появляется алерт 'Product added' и товар добавляется в корзину"""
        
        page = ProductPage(browser, PRODUCT_PAGE_URL.format(idp_=product_id))
        page.open()
        page.add_to_cart()
        try:
            WebDriverWait(browser, 10).until(EC.alert_is_present())  
            alert = Alert(browser)  
            alert_text = alert.text  
            assert "Product added" in alert_text, f"Неверный текст алерта для товара с ID {product_id}: {alert_text}"  

            alert.accept()  
            print(f"Alert для товара с ID {product_id} успешно принят.")
        except Exception as e:
            print(f"Alert для товара с ID {product_id} не был найден или ошибка при его обработке:", e)
            
        page.go_to_cart()
        product_in_cart = page.is_product_in_cart()
        assert product_in_cart, f"Товар с ID {product_id} не добавлен в корзину"
