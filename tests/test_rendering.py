import pytest
from utils.screenshot_maker import take_screenshot
import time, os
from PIL import ImageChops

@pytest.mark.parametrize("browser", ["chrome", "firefox"], indirect=True)
def test_site_up_and_visual_consistency(browser, name="difference", folder="tests/screenshots/diff_screen"):
    """Проверяем, что сайт работает и сравниваем скриншоты на визуальные различия"""

    path = os.path.join(folder, f"{name}.png")  

    browser.get("https://www.demoblaze.com/")
    
    assert "STORE" in browser.title
    
    image1 = take_screenshot(browser, name="home_page_loads")
    
    time.sleep(1)
    
    image2 = take_screenshot(browser, name="product_loads")
    
    diff = ImageChops.difference(image1, image2)

    if diff.getbbox():
        diff.save(path)
        assert False, "Изображения различаются!" 
    else:
        assert True
