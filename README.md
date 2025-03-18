## Структура проекта

```plaintext
Тестирование Demoblaze
│   .gitignore          
│   conftest.py         
│   locators.py         
│   pytest.ini         
│
├───archive            - Архив старых файлов (Реализация тестов по условиям 2КТ)
│       old_main.py
│       инфа.txt
│
├───components         - Модули UI-компонентов
│       auth_modal.py
│       custom_alert.py
│       login_modal.py
│       navigation_menu.py
│       order_modal.py
│       signup_modal.py
│
├───config             - Конфигурация проекта
│       config.py
│
├───pages              - Страницы Demoblaze
│       base_page.py
│       cart_page.py
│       main_page.py
│       product_page.py
│
├───tests              - Тесты Demoblaze
│       test_cart_page.py
│       test_login_modal.py
│       test_main_page.py
│       test_order_modal.py
│       test_product_page.py
│       test_signup_modal.py
│       test_smoke.py
│
├───utils              - Вспомогательные модули
│       data_generator.py - используется в тесте на регистрацию нового пользователя

