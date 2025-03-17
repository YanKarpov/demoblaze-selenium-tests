from .base_page import BasePage
from locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class MainPage(BasePage):
    """Главная страница"""

    def is_banner_visible(self):
        """Проверяет, отображается ли баннер"""
        return self.is_element_present(*MainPageLocators.BANNER)

    def is_login_button_clickable(self):
        """Проверяет, кликабельна ли кнопка логина"""
        return self.is_element_clickable(*MainPageLocators.LOGIN_BUTTON)

    def is_signup_button_clickable(self):
        """Проверяет, кликабельна ли кнопка регистрации"""
        return self.is_element_clickable(*MainPageLocators.SIGNUP_BUTTON)

    def is_nav_bar_visible(self):
        """Проверяет, есть ли навигационная панель"""
        return self.is_element_present(*MainPageLocators.NAV_BAR)

    def go_to_category(self, category_name):
        """Переходит в категорию"""
        categories = {
            "Laptops": MainPageLocators.CATEGORY_LAPTOPS,
            "Phones": MainPageLocators.CATEGORY_PHONES,
            "Monitors": MainPageLocators.CATEGORY_MONITORS,
        }
        if category_name in categories:
            print(f"Кликаем по категории {category_name}")
            self.click(*categories[category_name])

    def is_category_active(self, category_name):
        """Проверяет, что категория активна"""
        category_locator = {
            "Laptops": MainPageLocators.CATEGORY_LAPTOPS,
            "Phones": MainPageLocators.CATEGORY_PHONES,
            "Monitors": MainPageLocators.CATEGORY_MONITORS,
        }
        locator = category_locator[category_name]

        # Ожидание, пока элемент получит класс active
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(locator)
        )

        return "active" in self.get_element_attribute(locator[0], locator[1], "class")

    def is_products_displayed(self):
        """Проверяет, что есть товары на странице"""
        return self.is_element_present(*MainPageLocators.PRODUCT_ITEM)
