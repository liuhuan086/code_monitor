from rest_framework.decorators import action
from monitor.models import Leakage, Token, Task
from monitor.modules import task, leakage
from monitor.serializers import TokenSerializer, LeakageSerializer, TaskSerializer
from monitor import filter
from utils.baseviewsets import BasicViewSet
from django_filters.rest_framework import DjangoFilterBackend
from task.execute import perform_task_async


class TokenViewSet(BasicViewSet):
    queryset = Token.all()
    serializer_class = TokenSerializer


class LeakageViewSet(BasicViewSet):
    queryset = Leakage.all()
    serializer_class = LeakageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.LeakageFilter
    http_method_names = ['get', 'put', 'delete']

    @action(detail=False, methods=['delete'])
    def batch_del(self, request, pk=None):
        return leakage.batch_del_leakages(request)

    @action(detail=False, methods=['put'])
    def ignore_leakages(self, request, *args, **kwargs):
        return leakage.ignore_leakages(request)

    @action(detail=False, methods=['put'])
    def ignore_repos(self, request, *args, **kwargs):
        return leakage.ignore_repos(request)

    @action(detail=False, methods=['get'])
    def white_leakages(self, request, *args, **kwargs):
        return leakage.white_leakages(request)

    @action(detail=False, methods=['get'])
    def white_repos(self, request, *args, **kwargs):
        return leakage.white_repos(request)

    @action(detail=False, methods=['put'])
    def handle_leakages(self, request, *args, **kwargs):
        """对结果进行处理"""
        return leakage.handle_leakages(request)

    @action(detail=False, methods=['put'])
    def handled_leakages(self, request, *args, **kwargs):
        """查看已处理结果"""
        return leakage.handled_leakages(request)


class TaskViewSet(BasicViewSet):
    queryset = Task.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.TaskFilter

    def create(self, request, *args, **kwargs):
        task_res = super(TaskViewSet, self).create(request)
        perform_task_async.delay(task_res.data['id'])
        return task_res

    def destroy(self, request, *args, **kwargs):
        return task.del_task(self.get_object())

    @action(detail=False, methods=['delete'])
    def batch_del(self, request, pk=None):
        return task.batch_del_tasks(request)

    @action(detail=False, methods=['get'])
    def dashboard(self, request, pk=None):
        return task.get_dashboard()

    @action(detail=False, methods=['get'])
    def dashboard_detail(self, request, pk=None):
        return task.get_dashboard_detail(request)
