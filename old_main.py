from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

username = "Wolfychic"
password = "1111"
user_info = {
    "name": "Ян Карпов",
    "country": "Россия",
    "city": "Санкт-Петербург",
    "card": "1234 5678 9012 3456",
    "month": "12",
    "year": "2025",
}

driver = webdriver.Chrome()
driver.implicitly_wait(5)  
wait = WebDriverWait(driver, 10)  

driver.get("https://www.demoblaze.com/")

driver.find_element(By.ID, "signin2").click()
driver.find_element(By.ID, "sign-username").send_keys(username)
driver.find_element(By.ID, "sign-password").send_keys(password)
driver.find_element(By.XPATH, '//button[text()="Sign up"]').click()


try:
    alert = wait.until(EC.alert_is_present())  
    alert_text = alert.text
    assert "This user already exist" in alert.text, "Получили сообщение, которое не ожидали"
    alert.accept()

    if "This user already exist" in alert_text:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.ID, "login2").click()
        driver.find_element(By.ID, "loginusername").send_keys(username)
        driver.find_element(By.ID, "loginpassword").send_keys(password)
        driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
        assert wait.until(EC.presence_of_element_located((By.ID, "nameofuser"))), "Ошибка входа"

    for _ in range(3):  
        try:
            product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6")))
            product_link.click()
            break
        except Exception as e:
            print("Ошибка при клике на товар, повторяем попытку:", e)

    driver.find_element(By.XPATH, '//a[text()="Add to cart"]').click()
    
    alert = wait.until(EC.alert_is_present()) 
    alert.accept()
    
    driver.get("https://www.demoblaze.com/cart.html")
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Samsung galaxy s6')]"))), "Товар не добавлен в корзину"

    driver.find_element(By.XPATH, '//button[text()="Place Order"]').click()

    for field, value in user_info.items():
        driver.find_element(By.ID, field).send_keys(value)

    driver.find_element(By.XPATH, '//button[text()="Purchase"]').click()
    print("Заказ оформлен")

    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()
    assert driver.current_url == "https://www.demoblaze.com/index.html", "Не вернулись на главную страницу после оформления заказа"
    print("Окно подтверждения закрыто")

finally:
    driver.quit()