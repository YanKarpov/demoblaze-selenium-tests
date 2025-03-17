from locators import LoginModalLocators, MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.config import BASE_URL
from selenium.webdriver.common.by import By



class LoginModal:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        """Открывает модальное окно логина, кликая по кнопке логина на главной странице"""
        self.driver.get(BASE_URL)  
        self.driver.find_element(*MainPageLocators.LOGIN_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(LoginModalLocators.MODAL)
        )

    def is_modal_open(self):
        """Проверяет, открылось ли модальное окно"""
        return bool(self.driver.find_elements(*LoginModalLocators.MODAL))

    def enter_username(self, username):
        self.driver.find_element(*LoginModalLocators.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*LoginModalLocators.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        self.driver.find_element(*LoginModalLocators.LOGIN_BUTTON).click()

    def close(self):
        """Закрывает модальное окно"""
        self.driver.find_element(*LoginModalLocators.CLOSE_BUTTON).click()
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(LoginModalLocators.MODAL)
        )

    def is_logged_in(self):
        return self.driver.find_element(By.ID, "logout2").is_displayed()

    def is_error_message_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке"""
        return bool(self.driver.find_elements(*LoginModalLocators.ERROR_MESSAGE))
    
    def wait_for_login(self, timeout=10):
        """Ждёт, пока появится кнопка 'Log out' после успешного входа"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, "logout2"))
        )

