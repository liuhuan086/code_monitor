1. celery启动命令

   **需要先进入到项目根目录下**

   *启动worker*

   `celery worker -A task -l info`

   *启动beat*

   `celery beat -A task -l info`



2. 添加github token信息，可以实现登录GitHub网站

   配置文件:

   ​	/management/monitor/conf.py

   token='xxx'

   把xxx换成你的token信息



3. 定时任务配置

   配置文件:

   ​	/yyy_service/celery_tasks/celery.py

   ```
   # 任务配置文件
   app.conf.beat_schedule = {
   		# 可以更改mul-every-60-minute为自定义的任务计划的名称
       'mul-every-60-minute': {
           'task': 'celery_tasks.tasks.get_keyword',
           # seconds可以换成minutes，hours等
           'schedule': timedelta(seconds=60), # 更改定时任务的计划
           # crontab(minute='*/60')
           # 'args': ()
       }
   }
   ```



4. 启动项目

   1. 新建任务

      URL: http://127.0.0.1:8000/tasks/

      设置任务名和关键字
      
## 有用token
      6eb83db25e5596b6428488ace89a843b0c1e65da
## 创建数据库
CREATE DATABASE IF NOT EXISTS yyy DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

## 本地调试celery
celery -A task worker -l info -Q yyy.regular,yyy.execute -n yyy@%h