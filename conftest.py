import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import logger
from jira import JIRA
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(override=True)

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

jira, bug_type = init_jira()

def create_jira_issue(error_message):
    """Создание задачи в Jira."""
    if bug_type:
        jira_issue = jira.create_issue(
            fields={
                "project": {"key": "SEL"},
                "summary": "Ошибка при тестировании",
                "description": f"Ошибка в тесте: {error_message}\n\nДата: {datetime.now()}",
                "issuetype": {"id": bug_type.id}
            }
        )
        return jira_issue
    logger.error("Не удалось создать задачу, тип 'bug' не найден!")
    return None

def pytest_addoption(parser):
    """Добавление опции для выбора языка браузера."""
    parser.addoption(
        "--language", action="store", default="ru", help="Выбери язык для браузера"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Обработка отчётов по тестам (создание Jira задачи при ошибке или неожиданном прохождении теста)."""
    if call.when != "call":
        return  

    report = pytest.TestReport.from_item_and_call(item, call)

    if "xfail" in item.keywords and report.outcome == "passed":
        error_message = f"Тест '{item.name}' неожиданно прошёл (XPASS)"
        jira_issue = create_jira_issue(error_message)
        if jira_issue:
            logger.error(f"Задача в Jira создана: {jira_issue.key} по причине: {error_message}")
        return

    if report.failed and "xfail" not in item.keywords:
        error_message = f"Тест '{item.name}' упал с ошибкой: {report.longrepr}"
        jira_issue = create_jira_issue(error_message)
        if jira_issue:
            logger.error(f"Задача в Jira создана: {jira_issue.key} по причине ошибки: {error_message}")
            
    if "xfail" in item.keywords and report.outcome == "failed":
        error_message = f"Тест '{item.name}' ожидаемо не прошёл (XFALL)"
        logger.info(f"Тест '{item.name}' ожидаемо не прошёл, задач в Jira не будет создано.")

@pytest.fixture(scope="module")
def browser(request):
    """Фикстура для инициализации браузера с логированием."""
    language = request.config.getoption("language") or os.getenv("BROWSER_LANGUAGE", "ru")
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': language})

    logger.info("="*30 + f" НАЧАЛО ТЕСТОВ (Язык: {language}) " + "="*30)
    start_time = time.time()

    browser = webdriver.Chrome(options=options)
    yield browser

    elapsed_time = time.time() - start_time
    logger.info("="*30 + f" ЗАВЕРШЕНИЕ ТЕСТОВЫХ (Время: {elapsed_time:.2f} сек) " + "="*30)
    browser.quit()
