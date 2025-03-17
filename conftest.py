import pytest, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption(
        "--language", action="store", default="ru", help="Выбери язык для браузера"
    )


@pytest.fixture(scope="module")
def browser(request):
    language = request.config.getoption("language")
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': language})
    browser = webdriver.Chrome(options=options)
    yield browser
    time.sleep(5)
    browser.quit()
