# encoding: utf-8
# Date: 2019-09-19 13:45

__author__ = 'ryan.liu'

from django.conf import settings
import redis

RS = redis.Redis(**settings.REDIS_CONFIG)
