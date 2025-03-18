import pytest
from components.order_modal import OrderModal
from components.custom_alert import CustomAlert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException


@pytest.mark.smoke
class TestOrderModal:
    """Тесты модального окна оформления заказа"""

    def test_order_modal_opens(self, browser):
        """Проверяет, что модальное окно оформления заказа открывается"""
        page = OrderModal(browser)
        page.open()
        assert page.is_modal_open(), "Модальное окно оформления заказа не открылось"

    @pytest.mark.parametrize("order_data, expected_message", [
        ({"name": "Test User", "country": "Country", "city": "City", "credit_card": "1234 5678 9876 5432", "month": "12", "year": "2025"},
        "Thank you for your purchase!"),  # Успешное оформление
        ({"name": "", "country": "Country", "city": "City", "credit_card": "1234 5678 9876 5432", "month": "12", "year": "2025"},
        "please fill out name and creditcard."),  # Ошибка из-за пустого имени
        pytest.param({"name": "Test User", "country": "", "city": "City", "credit_card": "1234 5678 9876 5432", "month": "12", "year": "2025"},
                    "please fill out all fields", marks=pytest.mark.xfail(reason="Форма не отображает ошибку для пустой страны")),
        pytest.param({"name": "Test User", "country": "Country", "city": "", "credit_card": "1234 5678 9876 5432", "month": "12", "year": "2025"},
                    "please fill out all fields", marks=pytest.mark.xfail(reason="Форма не отображает ошибку для пустого города")),
        pytest.param({"name": "Test User", "country": "Country", "city": "City", "credit_card": "invalid_card", "month": "12", "year": "2025"},
                    "invalid credit card", marks=pytest.mark.xfail(reason="Некорректная карта не вызывает ошибку в системе"))
    ])
    def test_order(self, browser, order_data, expected_message):
        """Проверяет различные сценарии оформления заказа"""
        page = OrderModal(browser)
        page.open()

        page.enter_name(order_data["name"])
        page.enter_country(order_data["country"])
        page.enter_city(order_data["city"])
        page.enter_credit_card(order_data["credit_card"])
        page.enter_month(order_data["month"])
        page.enter_year(order_data["year"])

        try:
            page.place_order()

            try:
                alert = browser.switch_to.alert
                alert_text = alert.text.strip().lower() 
                alert.accept()  

                assert alert_text == expected_message.strip().lower(), f"Ожидаемый текст алерта: '{expected_message}', но получили: '{alert_text}'"
            except NoAlertPresentException:
                custom_alert = CustomAlert(browser)
                custom_alert.wait_for_alert()

                custom_alert.check_alert_text(expected_message)

                custom_alert.close_alert()

        except UnexpectedAlertPresentException:
            alert = browser.switch_to.alert
            alert_text = alert.text.strip().lower() 
            alert.accept()

            assert alert_text == expected_message.strip().lower(), f"Ожидаемый текст алерта: '{expected_message}', но получили: '{alert_text}'"
