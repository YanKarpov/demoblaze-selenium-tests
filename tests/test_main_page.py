import pytest
from pages.main_page import MainPage
from config.config import BASE_URL

@pytest.mark.smoke
class TestMainPageLoad:
    """Тесты, связанные с загрузкой главной страницы"""

    def test_home_page_loads(self, browser):
        """Проверяет, что главная страница загружается"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert page.is_banner_visible(), "Главный баннер не отображается"

    def test_page_title(self, browser):
        """Проверяет, что заголовок страницы корректный"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert browser.title == "STORE", "Некорректный заголовок страницы"

    def test_navigation_bar_present(self, browser):
        """Проверяет наличие навигационной панели"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert page.is_nav_bar_visible(), "Навигационная панель отсутствует"

@pytest.mark.regression
class TestMainPageButtons:
    """Тесты, связанные с кнопками"""

    def test_login_button_is_clickable(self, browser):
        """Проверяет, что кнопка 'Login' кликабельна"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert page.is_login_button_clickable(), "Кнопка логина не кликабельна"

    def test_signup_button_is_clickable(self, browser):
        """Проверяет, что кнопка 'Sign up' кликабельна"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert page.is_signup_button_clickable(), "Кнопка регистрации не кликабельна"

@pytest.mark.regression
class TestMainPageContent:
    """Тесты, связанные с контентом страницы"""

    def test_products_are_displayed(self, browser):
        """Проверяет, что на странице есть товары"""
        page = MainPage(browser, BASE_URL)
        page.open()
        assert page.is_products_displayed(), "Товары не отображаются"
