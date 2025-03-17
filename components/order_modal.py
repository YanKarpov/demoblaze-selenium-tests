from locators import CartPageLocators
from config.config import CART_PAGE_URL
from pages.base_page import BasePage

class OrderModal(BasePage):
    """Компонент модального окна оформления заказа"""
    
    def __init__(self, browser):
        super().__init__(browser, CART_PAGE_URL)

    def open(self):
        """Открывает страницу корзины и открывает модальное окно оформления заказа"""
        super().open()
        self.click(*CartPageLocators.PLACE_ORDER_BUTTON)  # Кликаем по кнопке для открытия модального окна
        self.wait_for_element(*CartPageLocators.ORDER_MODAL)  # Ожидаем появления модального окна

    def is_modal_open(self):
        """Проверяет, что модальное окно открылось"""
        return self.is_element_present(*CartPageLocators.ORDER_MODAL)

    def close(self):
        """Закрывает модальное окно"""
        self.click(*CartPageLocators.CLOSE_ORDER_MODAL_BUTTON)
        self.wait_for_element(*CartPageLocators.ORDER_MODAL, timeout=5)  # Ожидаем исчезновения модального окна

    def enter_name(self, name):
        """Вводит имя"""
        self.input_text(*CartPageLocators.NAME_FIELD, name)

    def enter_country(self, country):
        """Вводит страну"""
        self.input_text(*CartPageLocators.COUNTRY_FIELD, country)

    def enter_city(self, city):
        """Вводит город"""
        self.input_text(*CartPageLocators.CITY_FIELD, city)

    def enter_credit_card(self, credit_card):
        """Вводит номер кредитной карты"""
        self.input_text(*CartPageLocators.CREDIT_CARD_FIELD, credit_card)

    def enter_month(self, month):
        """Вводит месяц"""
        self.input_text(*CartPageLocators.MONTH_FIELD, month)

    def enter_year(self, year):
        """Вводит год"""
        self.input_text(*CartPageLocators.YEAR_FIELD, year)

    def place_order(self):
        """Нажимает кнопку оформления заказа"""
        self.click(*CartPageLocators.PLACE_ORDER_BUTTON_IN_MODAL)
