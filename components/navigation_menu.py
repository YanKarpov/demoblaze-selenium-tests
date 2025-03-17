from locators import NavigationMenuLocators

class NavigationMenu:
    def __init__(self, driver):
        self.driver = driver

    def go_to_home(self):
        self.driver.find_element(*NavigationMenuLocators.HOME_BUTTON).click()

    def go_to_contact(self):
        self.driver.find_element(*NavigationMenuLocators.CONTACT_BUTTON).click()

    def go_to_about(self):
        self.driver.find_element(*NavigationMenuLocators.ABOUT_BUTTON).click()

    def open_login_modal(self):
        self.driver.find_element(*NavigationMenuLocators.LOGIN_BUTTON).click()

    def open_signup_modal(self):
        self.driver.find_element(*NavigationMenuLocators.SIGNUP_BUTTON).click()
