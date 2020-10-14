# encoding: utf-8
# Date: 2019-08-09 16:50
from monitor.serializers import LeakageSerializer

__author__ = 'ryan.liu'

from utils import ServerExceptions, Err, make_response
from monitor.models import Leakage, Task


def batch_del_leakages(request):
    data = request.data
    if not data.get('leakage_ids'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    leakage_ids = data.getlist('leakage_ids')
    user_id = data['user_id']
    Leakage.mget_by(dict(id=leakage_ids, user_id=user_id)).update(status=Leakage.INVALID)
    return make_response({})


def ignore_repos(request):
    data = request.data
    if not data.get('repo_urls'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    user_id = data['user_id']
    repo_urls = data['repo_urls']
    repos = Task.objects.filter(user_id=user_id, leakage__repo_url__in=repo_urls, status=0).distinct()
    repo_list = [repo_url + '\n' for repo_url in repo_urls]
    for repo in repos:
        res = repo.ignore_repo + '\n'
        repo_list.append(res)
    Task.objects.filter(user_id=user_id, status=0).update(ignore_repo=repo_list)
    return make_response({})


def white_leakages(request):
    data = request.GET
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    user_id = data.get('user_id')
    leakages = Leakage.objects.filter(user_id=user_id, leakage_status=2)
    leakages_ser = LeakageSerializer(leakages, many=True)
    return make_response(leakages_ser.data)


def ignore_leakages(request):
    data = request.data
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    if not data.get('leakage_ids'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    user_id = data.get('user_id')
    leakage_ids = data['leakage_ids']
    Leakage.objects.filter(user_id=user_id, id__in=leakage_ids, leakage_status=0).update(leakage_status=2)
    return make_response({})


def white_repos(request):
    data = request.GET
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    user_id = data.get('user_id')
    tasks = Task.objects.filter(user_id=user_id, status=0).first()
    ignore_repo = tasks.ignore_repo
    return make_response(dict(ignore_repo))


def handle_leakages(request):
    data = request.data
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    if not data.get('leakage_ids'):
        raise ServerExceptions(Err.PARAMETER_ERROR)
    user_id = data.get('user_id')
    leakage_ids = data['leakage_ids']
    Leakage.objects.filter(user_id=user_id, id__in=leakage_ids, leakage_status=0).update(leakage_status=1)
    return make_response({})


def handled_leakages(request):
    data = request.GET
    if not data.get('user_id'):
        raise ServerExceptions(Err.USER_NOT_FOUND)
    user_id = data.get('user_id')
    leakages = Leakage.objects.filter(user_id=user_id, leakage_status=1)
    leakages_ser = LeakageSerializer(leakages, many=True)
    return make_response(leakages_ser.data)
