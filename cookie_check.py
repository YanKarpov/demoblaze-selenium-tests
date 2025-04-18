from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

options = Options()
options.add_argument("--auto-open-devtools-for-tabs")

driver = webdriver.Chrome(options=options)
driver.get("https://www.demoblaze.com/cart.html")

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


cart_items = driver.execute_script("""
    return new Promise((resolve) => {
        let token = document.cookie.split('; ').find(row => row.startsWith('tokenp_'))?.split('=')[1];
        let url = 'https://api.demoblaze.com/viewcart';
        let data = { cookie: token || document.cookie, flag: !!token };
        
        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(json => resolve(json));
    });
""")

time.sleep(15)
print(json.dumps(cart_items, indent=2))
driver.quit()
