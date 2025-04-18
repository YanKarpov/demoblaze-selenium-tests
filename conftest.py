import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv
from utils.logger import logger
from jira_logic.jira_client import init_jira
from jira_logic.reporter import JiraReporter

load_dotenv(override=True)

jira_client = None
jira_reporter = None


def pytest_addoption(parser):
    parser.addoption("--language", action="store", default="ru", help="Выбери язык для браузера")
    parser.addoption("--executor", action="store", default="local", help="Выбери режим запуска: local или remote")
    parser.addoption(
        "--jira", action="store", nargs="?", const=os.getenv("JIRA_DEFAULT_PROJECT", "SEL"), default=None,
        help="Включить Jira. Можно указать проект (например, --jira=ABC), или просто --jira (по умолчанию SEL)"
    )


def pytest_configure(config):
    global jira_client, jira_reporter
    jira_project_key = config.getoption("--jira")

    if jira_project_key:
        logger.info(f"Jira включена. Проект: {jira_project_key}")
        jira_client, bug_type = init_jira()

        if jira_client and bug_type:
            jira_reporter = JiraReporter(jira_client, bug_type, jira_project_key)
        else:
            logger.warning("Jira не инициализирована корректно.")
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

    if not jira_reporter:
        return

    if is_xfail and report.outcome == "passed":
        msg = f"Тест '{test_name}' неожиданно прошёл (XPASS)"
        issue = jira_reporter.create_issue(msg)
        jira_reporter.attach_screenshot(issue, browser, f"xpass_{test_name}")
    elif report.failed and not is_xfail:
        msg = f"Тест '{test_name}' упал с ошибкой: {report.longrepr}"
        issue = jira_reporter.create_issue(msg)
        jira_reporter.attach_screenshot(issue, browser, f"fail_{test_name}")
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
        selenium_grid_url = "http://10.11.23.23:5555/wd/hub"
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
