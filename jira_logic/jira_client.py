import os
from jira import JIRA
from utils.logger import logger

def init_jira():
    server = os.getenv("JIRA_SERVER")
    username = os.getenv("JIRA_USERNAME")
    api_key = os.getenv("JIRA_API_KEY")

    if not all([server, username, api_key]):
        logger.error("JIRA: переменные окружения не заданы.")
        return None, None

    jira_conn = JIRA(server=server, basic_auth=(username, api_key))
    bug_type = next((i for i in jira_conn.issue_types() if i.name.lower() in ["bug", "баг", "ошибка"]), None)
    
    if not bug_type:
        logger.error("JIRA: тип 'bug' не найден.")
        return jira_conn, None

    return jira_conn, bug_type
