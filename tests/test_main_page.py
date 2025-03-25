import pytest
from pages.main_page import MainPage
from config.config import MAIN_URL
from utils.screenshot_maker import take_screenshot
from locators import MainPageLocators 


@pytest.mark.smoke
class TestMainPageLoad:
    """Тесты, связанные с загрузкой главной страницы"""

    def test_home_page_loads(self, browser):
        """Проверяет, что главная страница загружается"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert page.is_banner_visible(), "Главный баннер не отображается"
        
        take_screenshot(browser, name="home_page_loads")

    def test_page_title(self, browser):
        """Проверяет, что заголовок страницы корректный"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert browser.title == "STORE", "Некорректный заголовок страницы"
        
        take_screenshot(browser, name="banner_display_check", element_locator=MainPageLocators.BANNER)  

    def test_navigation_bar_present(self, browser):
        """Проверяет наличие навигационной панели"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert page.is_nav_bar_visible(), "Навигационная панель отсутствует"
        
        take_screenshot(browser, name="nav_bar_present", element_locator=MainPageLocators.NAV_BAR)  


@pytest.mark.regression
class TestMainPageButtons:
    """Тесты, связанные с кнопками"""

    def test_login_button_is_clickable(self, browser):
        """Проверяет, что кнопка 'Login' кликабельна"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert page.is_login_button_clickable(), "Кнопка логина не кликабельна"
        
        take_screenshot(browser, name="login_button_check", element_locator=MainPageLocators.LOGIN_BUTTON)

    def test_signup_button_is_clickable(self, browser):
        """Проверяет, что кнопка 'Sign up' кликабельна"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert page.is_signup_button_clickable(), "Кнопка регистрации не кликабельна"
        
        take_screenshot(browser, name="signup_button_check", element_locator=MainPageLocators.SIGNUP_BUTTON)


@pytest.mark.regression
class TestMainPageContent:
    """Тесты, связанные с контентом страницы"""

    def test_products_are_displayed(self, browser):
        """Проверяет, что на странице есть товары"""
        page = MainPage(browser, MAIN_URL)
        page.open()
        assert page.is_products_displayed(), "Товары не отображаются"
        
        take_screenshot(browser, name="products_display_check", element_locator=MainPageLocators.PRODUCT_ITEM)
