import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.logger import logger
from utils.screenshot_maker import take_screenshot
from jira import JIRA
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

jira = None
bug_type = None
jira_project_key = None


def init_jira():
    """Инициализация подключения к Jira."""
    server = os.getenv("JIRA_SERVER")
    username = os.getenv("JIRA_USERNAME")
    api_key = os.getenv("JIRA_API_KEY")

    if not all([server, username, api_key]):
        logger.error("Ошибка: переменные окружения для Jira не заданы!")
        return None, None

    jira_conn = JIRA(server=server, basic_auth=(username, api_key))
    bug = next((i for i in jira_conn.issue_types() if i.name.lower() in ["bug", "баг", "ошибка"]), None)
    if not bug:
        logger.error("Тип задачи 'bug' не найден!")
    return jira_conn, bug


def attach_screenshot(jira_issue, browser, test_name):
    """Создание скриншота и прикрепление его к задаче."""
    if not browser:
        return
    screenshot = take_screenshot(browser, name=test_name)
    path = screenshot.filename
    with open(path, "rb") as f:
        jira.add_attachment(issue=jira_issue.key, attachment=f, filename=os.path.basename(path))
    logger.info(f"Скриншот добавлен к задаче {jira_issue.key}: {path}")


def create_issue_with_optional_screenshot(error_message, browser=None, test_name=""):
    """Создание задачи с опциональным скриншотом."""
    issue = create_jira_issue(error_message)
    if issue:
        logger.error(f"Задача в Jira создана: {issue.key} по причине: {error_message}")
        if browser:
            attach_screenshot(issue, browser, test_name)
    return issue


def create_jira_issue(error_message):
    """Создание задачи в Jira."""
    if jira and bug_type and jira_project_key:
        return jira.create_issue(fields={
            "project": {"key": jira_project_key},
            "summary": "Ошибка при тестировании",
            "description": f"Ошибка в тесте: {error_message}\n\nДата: {datetime.now()}",
            "issuetype": {"id": bug_type.id}
        })
    logger.error("Не удалось создать задачу в Jira — Jira не инициализирована или не указан проект.")
    return None


def pytest_addoption(parser):
    parser.addoption("--language", action="store", default="ru", help="Выбери язык для браузера")
    parser.addoption("--executor", action="store", default="local", help="Выбери режим запуска: local или remote")
    parser.addoption(
        "--jira", action="store", nargs="?", const=os.getenv("JIRA_DEFAULT_PROJECT", "SEL"), default=None,
        help="Включить Jira. Можно указать проект (например, --jira=ABC), или просто --jira (по умолчанию SEL)"
    )


def pytest_configure(config):
    global jira, bug_type, jira_project_key
    jira_project_key = config.getoption("--jira")
    if jira_project_key:
        logger.info(f"Jira включена. Проект: {jira_project_key}")
        jira, bug_type = init_jira()
    else:
        logger.info("Jira отключена.")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when != "call":
        return
    report = pytest.TestReport.from_item_and_call(item, call)
    browser = item.funcargs.get("browser")

    is_xfail = "xfail" in item.keywords
    test_name = item.name

    if is_xfail and report.outcome == "passed":
        msg = f"Тест '{test_name}' неожиданно прошёл (XPASS)"
        create_issue_with_optional_screenshot(msg, browser, f"xpass_{test_name}")
    elif report.failed and not is_xfail:
        msg = f"Тест '{test_name}' упал с ошибкой: {report.longrepr}"
        create_issue_with_optional_screenshot(msg, browser, f"fail_{test_name}")
    elif is_xfail and report.outcome == "failed":
        logger.info(f"Тест '{test_name}' ожидаемо не прошёл (XFALL), задача в Jira не создаётся.")


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def browser(request):
    language = request.config.getoption("language") or os.getenv("BROWSER_LANGUAGE", "ru")
    executor = request.config.getoption("executor")
    test_name = request.node.name

    logger.info("="*30 + f" НАЧАЛО ТЕСТА: {test_name} (Язык: {language}, Executor: {executor}) " + "="*30)
    start_time = time.time()

    browser_name = request.param

    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    if executor == "remote":
        selenium_grid_url = "http://192.168.56.1:5555/wd/hub"
        browser = webdriver.Remote(command_executor=selenium_grid_url, options=options)
    else:
        if browser_name == "chrome":
            browser = webdriver.Chrome(options=options)
        else:
            browser = webdriver.Firefox(options=options)

    yield browser

    elapsed_time = time.time() - start_time
    logger.info("="*30 + f" ЗАВЕРШЕНИЕ ТЕСТА: {test_name} (Время: {elapsed_time:.2f} сек) " + "="*30)
    browser.quit()
