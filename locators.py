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

class ProductCardLocators:
    """Локаторы для карточек товаров"""
    PRODUCT_NAME = (By.CLASS_NAME, "card-title")
    PRODUCT_PRICE = (By.CLASS_NAME, "card-price")
    PRODUCT_LINK = (By.TAG_NAME, "a")  

class CartPageLocators:
    """Локаторы для корзины"""
    CART_TABLE = (By.ID, "tbodyid")  
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Place Order')]")
    DELETE_BUTTONS = (By.XPATH, "//a[contains(text(), 'Delete')]")

