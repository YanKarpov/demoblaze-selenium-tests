from utils.screenshot_maker import take_screenshot
import time
from PIL import ImageChops

def test_site_up_and_visual_consistency(browser):
    """Проверяем, что сайт работает и сравниваем скриншоты на визуальные различия"""

    browser.get("https://www.demoblaze.com/")
    
    assert "STORE" in browser.title
    
    image1 = take_screenshot(browser, name="home_page_loads")
    
    time.sleep(1)
    
    image2 = take_screenshot(browser, name="product_loads")
    
    diff = ImageChops.difference(image1, image2)

    if diff.getbbox():

        diff.save("difference.png")

        assert False, "Изображения различаются!" 
    else:
        assert True  