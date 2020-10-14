# encoding: utf-8
# Date: 2019-08-14 11:28

__author__ = 'ryan.liu'

from django_filters.rest_framework import FilterSet, filters
from monitor.models import Leakage, Task, Token


class TokenFilter(FilterSet):
    user_id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Token
        fields = ['user_id', 'token']


class TaskFilter(FilterSet):
    user_id = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    keyword = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['user_id', 'name', 'keyword']


class LeakageFilter(FilterSet):
    user_id = filters.CharFilter(lookup_expr='icontains')
    keyword = filters.CharFilter(lookup_expr='icontains')
    file_name = filters.CharFilter(lookup_expr='icontains')
    repo_name = filters.CharFilter(lookup_expr='icontains')
    leakage_status = filters.CharFilter(lookup_expr='icontains')
    task = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Leakage
        fields = ['user_id', 'keyword', 'file_name', 'repo_name', 'leakage_status', 'task__id']
