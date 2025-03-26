import os
from datetime import datetime
from PIL import Image

def take_screenshot(driver, name="screenshot", element_locator=None, folder="tests/screenshots/"):
    os.makedirs(folder, exist_ok=True)  
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
    path = os.path.join(folder, f"{name}_{timestamp}.png")  
    
    if element_locator:
        element = driver.find_element(*element_locator)
        element.screenshot(path)
    else:
        driver.save_screenshot(path)

    print(f"Скриншот сохранён: {path}")
    
    return Image.open(path)