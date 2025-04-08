import os
from jira import JIRA
from dotenv import load_dotenv
from time import datetime

load_dotenv(override=True)

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")


jira = JIRA(server=JIRA_SERVER, 
            basic_auth=(JIRA_USERNAME, JIRA_API_KEY)
)

for i in jira.issue_types():
    if i.name.lower() in ["bug", "баг", "ошибка"]:
        bug_type = i

jira_issue = jira.create_issue(
    {
        "project": {"key": "SEL"},
        "summary": "Задача тестовая",
        "description": f"Ахтунг НАЗВАНИЕ_ОШИБКИ\n\nДата:{datetime.datetime.now()}",
        "IssueType": {"id": "10038"}
    }
)

jira.add_attachment(jira_issue.key, "Безымянный.png")



