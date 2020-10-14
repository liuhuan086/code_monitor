from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery('wm-mission', include=['task.regular', 'task.execute'])

#  使用CELERY_ 作为前缀，在settings中写配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 发现任务文件每个app下的task.py
app.autodiscover_tasks()

# 时区设置
app.conf.timezone = 'Asia/Shanghai'

# 不使用utc时间
app.conf.enable_utc = False

# 定时任务时间
regular_task = timedelta(hours=1)

# 把定时任务时间转换成时间戳格式，seconds可以换成minutes，hours等
regular_time = regular_task.seconds

# 任务配置文件
app.conf.beat_schedule = {
    'search_keyword': {
        'task': 'task.regular.bulk_perform_task_by_keywords',
        'schedule': crontab(hour=23, minute=00),
        # 'schedule': timedelta(hours=7),
        # 'args': ()
    },

    'search_repo': {
        'task': 'task.regular.bulk_perform_task_by_repo',
        'schedule': crontab(hour=23, minute=30),
        # 'schedule': timedelta(hours=23, minutes=30),
        # 'args': ()
    },

    'set_daily_list': {
        'task': 'task.regular.update_dashboard_daily',
        # 'schedule': crontab(hour=17, minute=15),
        'schedule': timedelta(hours=0, minutes=0),
        # 'args': ()
    }
}

app.conf.task_routes = {
    'task.execute.perform_task_async': {'queue': 'guanshu.execute'},
    'task.regular.bulk_perform_task_by_keywords': {'queue': 'guanshu.regular'},
    'task.regular.bulk_perform_task_by_repo': {'queue': 'guanshu.regular'},
    'task.regular.update_dashboard_daily': {'queue': 'guanshu.regular'},
}
