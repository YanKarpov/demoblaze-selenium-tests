from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы для главной страницы"""
    BANNER = (By.ID, "contcar")  
    NAV_BAR = (By.CLASS_NAME, "navbar")  
    LOGIN_BUTTON = (By.ID, "login2")  
    SIGNUP_BUTTON = (By.ID, "signin2")  
    PRODUCT_ITEM = (By.CLASS_NAME, "card")  

    # Локаторы для категорий
    CATEGORY_LAPTOPS = (By.XPATH, "//a[contains(text(), 'Laptops')]")
    CATEGORY_PHONES = (By.XPATH, "//a[contains(text(), 'Phones')]")
    CATEGORY_MONITORS = (By.XPATH, "//a[contains(text(), 'Monitors')]")

class NavigationMenuLocators:
    """Локаторы для верхнего меню"""
    HOME_BUTTON = (By.LINK_TEXT, "Home")
    CONTACT_BUTTON = (By.LINK_TEXT, "Contact")
    ABOUT_BUTTON = (By.LINK_TEXT, "About us")
    LOGIN_BUTTON = (By.ID, "login2")  
    SIGNUP_BUTTON = (By.ID, "signin2")  

class SignUpModalLocators:
    """Локаторы для модального окна регистрации"""
    MODAL = (By.ID, "signInModal")  
    USERNAME_INPUT = (By.ID, "sign-username")
    PASSWORD_INPUT = (By.ID, "sign-password")
    SIGNUP_BUTTON = (By.XPATH, "//button[contains(text(), 'Sign up')]")
    CLOSE_BUTTON = (By.XPATH, "//div[@id='signInModal']//button[@class='close']")

class LoginModalLocators:
    """Локаторы для модального окна входа"""
    MODAL = (By.ID, "logInModal") 
    USERNAME_INPUT = (By.ID, "loginusername")
    PASSWORD_INPUT = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//div[@id='logInModal']//button[text()='Log in']")
    CLOSE_BUTTON = (By.XPATH, "//div[@id='logInModal']//button[contains(@class, 'close')]")

class ProductPageLocators:
    """Локаторы для страницы товара"""
    PRODUCT_NAME = (By.CLASS_NAME, "name")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "div.product-image")
    PRODUCT_PRICE = (By.CLASS_NAME, "price-container")
    PRODUCT_DESCRIPTION = (By.ID, "more-information")
    ADD_TO_CART_BUTTON = (By.XPATH, "//a[contains(text(), 'Add to cart')]")

    PRODUCT_ADDED_ALERT = (By.CSS_SELECTOR, ".alert-success")  # Примерный локатор для алерта
    CART_BUTTON = (By.ID, "cartur")

class CartPageLocators:
    """Локаторы для корзины"""
    CART_TABLE = (By.ID, "tbodyid")  # Таблица с товарами в корзине
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button[data-target='#orderModal']")
    DELETE_BUTTON = (By.XPATH, "//a[starts-with(@onclick, 'deleteItem(')]")  # Локатор для кнопки удаления товара
    PRODUCT_NAME_IN_CART = (By.XPATH, "//tbody[@id='tbodyid']//tr[@class='success']/td[2]")  # Локатор для названия товара в корзине
    ORDER_MODAL = (By.ID, "orderModal")
    CLOSE_ORDER_MODAL_BUTTON = (By.CSS_SELECTOR, ".close-order-modal")
    PLACE_ORDER_BUTTON_IN_MODAL = (By.CSS_SELECTOR, "button.btn.btn-primary[onclick='purchaseOrder()']")

    NAME_FIELD = (By.ID, "name")
    COUNTRY_FIELD = (By.ID, "country")
    CITY_FIELD = (By.ID, "city")
    CREDIT_CARD_FIELD = (By.ID, "card")
    MONTH_FIELD = (By.ID, "month")
    YEAR_FIELD = (By.ID, "year")



