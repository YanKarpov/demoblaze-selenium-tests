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

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")

jira = JIRA(server=JIRA_SERVER, 
            basic_auth=(JIRA_USERNAME, JIRA_API_KEY))

def create_jira_issue(error_message):
    for i in jira.issue_types():
        if i.name.lower() in ["bug", "баг", "ошибка"]:
            bug_type = i

    jira_issue = jira.create_issue(
        fields={
            "project": {"key": "SEL"},  
            "summary": "Ошибка при тестировании",
            "description": f"Ошибка в тесте: {error_message}\n\nДата: {datetime.now()}",
            "issuetype": {"id": bug_type.id}
        }
    )
    return jira_issue

def pytest_addoption(parser):
    parser.addoption(
        "--language", action="store", default="ru", help="Выбери язык для браузера"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if "xfail" in item.keywords:
        if call.excinfo is None:  
            error_message = f"Тест {item.name} неожиданно прошел."
            jira_issue = create_jira_issue(error_message)
            logger.error(f"Задача в Jira создана: {jira_issue.key} по причине: {error_message}")
        return  

    if call.excinfo is not None:
        error_message = str(call.excinfo)
        jira_issue = create_jira_issue(error_message)
        logger.error(f"Задача в Jira создана: {jira_issue.key} по причине ошибки: {error_message}")

@pytest.fixture(scope="module")
def browser(request):
    """Фикстура для инициализации браузера с логированием."""
    language = request.config.getoption("language")
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': language})

    logger.info(f"\n===== НАЧАЛО ТЕСТОВОЙ СЕССИИ (Язык: {language}) =====")
    start_time = time.time()

    browser = webdriver.Chrome(options=options)
    yield browser

    elapsed_time = time.time() - start_time
    logger.info(f"===== ЗАВЕРШЕНИЕ ТЕСТОВОЙ СЕССИИ (Время: {elapsed_time:.2f} сек) =====\n")
    browser.quit()
