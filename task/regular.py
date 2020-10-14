from __future__ import absolute_import, unicode_literals
from celery import shared_task
# import django, os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')
# django.setup()
from monitor.models import Task
from monitor.modules.task import search_keyword, search_repo, set_daily_data
from django.db import close_old_connections
from concurrent.futures import ThreadPoolExecutor


def start_search(func):
    tasks = Task.all()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(func, tasks)
    close_old_connections()


@shared_task
def bulk_perform_task_by_keywords():
    start_search(search_keyword)


@shared_task
def bulk_perform_task_by_repo():
    start_search(search_repo)


@shared_task
def update_dashboard_daily():
    set_daily_data()
    close_old_connections()


if __name__ == '__main__':
    bulk_perform_task_by_keywords()
    bulk_perform_task_by_repo()
