# encoding: utf-8
# Date: 2019-07-15 18:07

__author__ = 'ryan.liu'

from django.core.exceptions import PermissionDenied
from rest_framework import exceptions
from rest_framework.views import set_rollback
from django.http import JsonResponse, Http404
import logging

logger = logging.getLogger(__name__)


def _error_response(request, message, code, http_code):
    resp = dict(
        message=message,
        link=request.path,
        codes=[code],
    )
    return JsonResponse(resp, status=http_code)


class Err(object):
    UNKNOWN_ERROR = 500001, '未知错误', 500
    PARAMETER_ERROR = 400121, '缺少参数', 400
    TOKEN_NOT_FOUND = 400122, '未添加token', 400
    TOKEN_LENGTH_ERROR = 400123, '长度不正确', 400
    TOKEN_EXISTED = 400124, 'token已存在', 400
    USER_NOT_FOUND = 400125, '用户不存在', 400
    TASK_NOT_FOUND = 400126, '任务不存在', 400
    TASK_EXISTED = 400127, '任务已存在', 400
    KEYWORD_EXISTED = 4001288, '关键字已存在', 400
    NO_TASK_ADDED = 4001289, '还未添加任务', 400
    TASK_OR_KEYWORD_EXISTED = 400130, '相同任务名或关键字已存在', 400


class ServerExceptions(Exception):
    pass


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """

    if isinstance(exc, Http404):
        return _error_response(context['request'], '没有这个地址', 404000, 404)
    elif isinstance(exc, PermissionDenied):
        return _error_response(context['request'], '权限不足', 401000, 400)

    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = exc.detail

        set_rollback()
        return _error_response(context['request'], data, 400001, 400)

    if isinstance(exc, ServerExceptions):
        args = exc.args[0]
        logger.error('error code: {}, msg: {}, http_code: {}'.format(args[0], args[1], args[2]))
        return _error_response(request=context['request'], message=args[1], code=args[0], http_code=args[2])

    if isinstance(exc, ConnectionError):
        logger.error('connection error, path:{}'.format(context['request']))
        return _error_response(request=context['request'], message='connection error', code=500001, http_code=500)

    return _error_response(request=context['request'], message="unknow error", code=500001, http_code=500)
