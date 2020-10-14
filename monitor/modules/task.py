import datetime
import json
import time
import pandas as pd
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.utils import timezone
from github import GithubException, RateLimitExceededException
from urllib3.exceptions import ReadTimeoutError
from monitor.models import Leakage, Task
import hashlib
from monitor.modules.token import new_session, reset_token
from utils import make_response, Err, ServerExceptions
from collections import Counter
import logging
from utils.redistool import RS

logger = logging.getLogger(__name__)


def format_fragments(text_matches):
    return ''.join([f['fragment'] for f in text_matches])


def update_task_time(task):
    cur_time = datetime.datetime.now()
    next_search_time = cur_time + datetime.timedelta(hours=1)
    task.finished_time = cur_time
    task.next_search_time = next_search_time
    task.save()


def search_repo(task):
    """查询仓库"""
    total = 0
    session, token = new_session()
    while True:
        try:
            response = session.search_repositories(task.keyword, sort='stars', order='desc')
            total = min(response.totalCount, 1000)
            break
        except ReadTimeoutError as e:
            print('连接超时，重新连接中...')
            continue
        except GithubException as e:
            if 'abuse-rate-limits' in e.data.get('documentation_url'):
                print('访问频率限制，正在重新尝试...')
                session, token = reset_token(session, token)
            else:
                logger.exception(e)
    per_page = 50
    max_page = (total // per_page) if (not total % per_page) else (total // per_page + 1)
    pages = min(max_page, 20)
    page = 0

    while page < pages:
        try:
            page_content = response.get_page(page)
            parse_repo_page(task, page_content)
            page += 1

        except RateLimitExceededException as e:
            print('GithubException...')
            if 'abuse-rate-limits' in e.data.get('documentation_url'):
                session, token = reset_token(session, token)
            else:
                logger.exception(e)
            continue
        # 防止由于网络原因导致的获取失败
        except ReadTimeoutError:
            print('ReadTimeoutError..')
            continue

        except Exception as e:
            print("Exception...")
            logger.exception(e)
            continue

    print('任务：搜索{}仓库完毕'.format(task.name))
    update_task_time(task)


def parse_repo_page(task, page_content):
    my_hash = hashlib.md5()
    leakage_num = 0
    ignore_repos = Task.objects.values_list('ignore_repo', flat=True).filter(status=0, user_id=task.user_id)
    ignore_users = Task.objects.values_list('ignore_org', flat=True).filter(status=0, user_id=task.user_id)
    for github_file in page_content:
        details = github_file._rawData
        owner = details.get('owner')
        keyword = details.get('name')

        if keyword in ignore_repos:
            continue

        if owner.login in ignore_users:
            continue

        user_name = owner.get('login')
        hash_result = str(user_name) + str(keyword) + str(owner)
        my_hash.update(hash_result.encode('utf-8'))
        hash_value = my_hash.hexdigest()
        leakage = Leakage.get_by(dict(user_id=task.user_id, hash_value=hash_value))
        if leakage:
            if leakage.filter(leakage_status=1):
                leakage.update(create_time=timezone.now(), leakage_status=0)
            continue

        Leakage.new(dict(
            keyword=task.keyword,
            sha='',
            fragment='',
            html_url='',
            file_name='',
            repo_name=details.get('full_name'),
            repo_url=details.get('html_url'),
            user_avatar=owner.get('avatar_url'),
            user_name=owner.get('login'),
            user_url=owner.get('html_url'),
            hash_value=hash_value,
            user_id=task.user_id,
            task=task,
        ))
        leakage_num += 1
    print('repo发现新的疑似泄漏信息, leakage count: {}'.format(leakage_num))


def parse_keyword_page(task, page_content):
    my_hash = hashlib.md5()
    leakage_num = 0
    ignore_repos = Task.objects.values_list('ignore_repo', flat=True).filter(status=1, user_id=task.user_id)
    ignore_users = Task.objects.values_list('ignore_org', flat=True).filter(status=1, user_id=task.user_id)
    for github_file in page_content:
        repo = github_file.repository
        owner = repo.owner

        if repo in ignore_repos:
            continue

        if owner.login in ignore_users:
            continue

        hash_result = github_file.sha + owner.login + task.keyword
        my_hash.update(hash_result.encode('utf-8'))
        hash_value = my_hash.hexdigest()
        leakage = Leakage.get_by(dict(user_id=task.user_id, hash_value=hash_value))
        if leakage:
            if leakage.filter(leakage_status=1):
                leakage.update(create_time=timezone.now(), leakage_status=0)
            continue

        Leakage.new(dict(
            keyword=task.keyword,
            sha=github_file.sha,
            fragment=format_fragments(github_file.text_matches),
            html_url=github_file.html_url,
            file_name=github_file.name,
            repo_name=repo.name,
            repo_url=repo.html_url,
            user_avatar=repo.owner.avatar_url,
            user_name=repo.owner.login,
            user_url=repo.owner.html_url,
            hash_value=hash_value,
            user_id=task.user_id,
            task=task,
        ))
        leakage_num += 1
    print('keyword发现新的疑似泄漏信息, leakage count: {}'.format(leakage_num))


def search_keyword(task):
    """查询关键字"""
    total = 0
    session, token = new_session()
    while True:
        try:
            response = session.search_code(task.keyword, sort='indexed', order='desc', highlight=True)
            total = min(response.totalCount, 1000)
            break
        except ReadTimeoutError as e:
            print('连接超时，重新连接中...')
            continue
        except GithubException as e:
            if 'abuse-rate-limits' in e.data.get('documentation_url'):
                print('访问频率限制，正在重新尝试...')
                session, token = reset_token(session, token)
            else:
                logger.exception(e)
            continue

    per_page = 50
    max_page = (total // per_page) if (not total % per_page) else (total // per_page + 1)
    pages = min(max_page, 20)
    page = 0
    while page < pages:
        try:
            page_content = response.get_page(page)
            page += 1
        except RateLimitExceededException:
            print('访问限制')
            session, token = reset_token(session, token)
            continue

        except GithubException as e:
            print('GithubException...')
            if 'abuse-rate-limits' in e.data.get('documentation_url'):
                session, token = reset_token(session, token)
            else:
                logger.exception(e)
            continue
        # 防止由于网络原因导致的获取失败
        except ReadTimeoutError:
            print('ReadTimeoutError..')
            continue
        parse_keyword_page(task, page_content)

    print(' 任务：{}搜索代码完毕'.format(task.name))
    update_task_time(task)


def perform_task(task_id):
    from task.execute import perform_task_async
    perform_task_async.delay(task_id, )


def del_task(request):
    data = request.data
    if not data.get('task_id'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    task_id = data['task_id']
    user_id = data['user_id']
    Leakage.mget_by(dict(task_id=task_id, user_id=user_id)).update(status=Leakage.INVALID)
    Task.get_by(dict(id=task_id, user_id=user_id)).update(status=Task.INVALID)
    return make_response({})


def batch_del_tasks(request):
    data = request.data
    if not data.get('task_ids'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    task_ids = data.getlist('task_ids')
    user_id = data['user_id']
    Leakage.mget_by(dict(task_id=task_ids, user_id=user_id)).update(status=Leakage.INVALID)
    Task.mget_by(dict(id=task_ids, user_id=user_id)).update(status=Task.INVALID)
    return make_response({})


# ### 时间戳格式
def get_dashboard_detail(request):
    data = request.query_params.dict()
    if data.get('start_date') or data.get('end_date'):
        start_date = data.get('start_date')
        start_date = int(start_date) / 1000000
        start = time.localtime(start_date)
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', start)

        end_date = data.get('end_date')
        end_date = int(end_date) / 1000000
        end = time.localtime(end_date)
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', end)
    else:
        cur_time = time.time()
        int_cur_time = int(cur_time)
        start = time.localtime(int_cur_time)
        year = time.strftime('%Y', start)
        start_time = '{}-{}-{}'.format(year, '01', '01')
        end_time = '{}-{}-{}'.format(year, '12', '31')

    keywords = Leakage.objects.filter(
        create_time__range=(start_time, end_time)).values_list('keyword', flat=True)
    aaa = Counter(keywords)
    pie_sorter = sorted(aaa.items(), key=lambda dic: dic[1], reverse=True)
    pie_dic = [{'x': xxx[0], 'y': xxx[1]} for xxx in pie_sorter]
    pie_dic_data = pie_dic[0:5]
    total_nums = 0
    fifth_nums = 0
    for i in pie_dic:
        total_nums += i['y']
    for j in pie_dic[:5]:
        fifth_nums += j['y']
    margin = total_nums - fifth_nums
    if margin != 0:
        pie_dic_data.append({'x': '其他', 'y': margin})
    tags = [{'name': x, 'value': y} for x, y in aaa.items()]
    return make_response(dict(pieData=pie_dic_data, tags=tags))


def get_daily_data():
    finally_res = {}
    dic_list = []
    total = 0
    res = 0

    try:
        first_data = Leakage.objects.filter(status=1).last()
        first_data_time = first_data.create_time
        cur_day = datetime.datetime.now()
        interval_time = cur_day - first_data_time
        interval_day = interval_time.days

        struct_times = Leakage.objects.filter(status=1).annotate(
            year=ExtractYear('create_time'),
            month=ExtractMonth('create_time'),
            day=ExtractDay('create_time')
        ).values('year', 'month', 'day')
        pandas_data = pd.DataFrame(struct_times)
        pandas_size = pandas_data.groupby(["year", "month", "day"]).size()
        for dates, count in pandas_size.items():
            dic = {}
            for x in range(len(dates)):
                res = str(dates[0]) + '-' + str('%02d' % dates[1] + '-' + str('%02d' % dates[2]))
            dic['x'] = res
            dic['y'] = count
            dic_list.append(dic)
            total += count

        if interval_day == 0:
            daily_avg = total / 1
        else:
            daily_avg = total / interval_day

        finally_res['total'] = total
        finally_res['dayAvg'] = daily_avg
        finally_res['dailylist'] = dic_list

        return finally_res

    except AttributeError or KeyError:
        # 当首次运行时，没有任何数据，设置初始值
        dic = {'x': 0, 'y': 0}
        dic_list.append(dic)
        finally_res['total'] = 0
        finally_res['dayAvg'] = 0
        finally_res['dailylist'] = dic_list

        return finally_res


def set_daily_data():
    daily_data = get_daily_data()
    RS.set('daily_data', json.dumps(daily_data))
    RS.expire('daily_data', 86400)


def get_dashboard():
    if not RS.get('daily_data'):
        set_daily_data()
    daily_data_bytes = RS.get('daily_data')
    finally_data = json.loads(daily_data_bytes)
    return make_response(finally_data)
