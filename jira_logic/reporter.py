import os
from datetime import datetime
from utils.logger import logger
from utils.screenshot_maker import take_screenshot

class JiraReporter:
    def __init__(self, jira_client, bug_type, project_key):
        self.jira = jira_client
        self.bug_type = bug_type
        self.project_key = project_key

    def create_issue(self, message):
        if not all([self.jira, self.bug_type, self.project_key]):
            logger.error("JIRA: невозможно создать задачу, не хватает параметров.")
            return None

        issue = self.jira.create_issue(fields={
            "project": {"key": self.project_key},
            "summary": "Ошибка при тестировании",
            "description": f"{message}\n\nДата: {datetime.now()}",
            "issuetype": {"id": self.bug_type.id}
        })

        logger.error(f"JIRA: создана задача {issue.key}")
        return issue

    def attach_screenshot(self, issue, browser, test_name):
        if not browser:
            return
        screenshot = take_screenshot(browser, name=test_name)
        path = screenshot.filename
        with open(path, "rb") as f:
            self.jira.add_attachment(issue=issue.key, attachment=f, filename=os.path.basename(path))
        logger.info(f"JIRA: скриншот прикреплён к {issue.key}: {path}")
