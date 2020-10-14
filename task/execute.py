# encoding: utf-8
# Date: 2019-08-20 16:46

__author__ = 'ryan.liu'

from task.celery import app

from monitor.models import Task
from monitor.modules.task import search_keyword, search_repo


@app.task
def perform_task_async(task_id):
    task = Task.get(task_id)
    if not task:
        return
    search_keyword(task)
    search_repo(task)


