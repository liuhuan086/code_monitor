# encoding: utf-8
# Date: 2019-07-19 14:30

__author__ = 'ryan.liu'

from rest_framework import status
from rest_framework.response import Response
from utils.baseexception import ServerExceptions, Err


def make_response(data):
    return Response(data=data, status=status.HTTP_200_OK)


class Singleton(type):
    """Usage:
    class Foo(Base):
        __metaclass__ = Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def valid_token(token):
    if len(token) != 40:
        raise ServerExceptions(Err.TOKEN_LENGTH_ERROR)
