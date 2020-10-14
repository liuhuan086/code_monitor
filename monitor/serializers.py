from rest_framework.validators import UniqueTogetherValidator
from monitor.models import Leakage, Token, Task
from rest_framework import serializers


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'token', 'user_id')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'keyword', 'user_id')

        validators = [
            UniqueTogetherValidator(
                queryset=Task.all(),
                fields=['user_id', 'name'],
                message='相同任务名已存在'
            ),
            UniqueTogetherValidator(
                queryset=Task.all(),
                fields=['user_id', 'keyword'],
                message='相同关键字已存在'
            ),
        ]

    def to_representation(self, instance):
        return dict(
            id=instance.id,
            name=instance.name,
            keyword=instance.keyword,
            create_time=instance.first_search_time.strftime("%Y-%m-%d %H:%M:%S"),
            next_search_time=instance.next_search_time.strftime("%Y-%m-%d %H:%M:%S"),
            finished_time=instance.finished_time.strftime("%Y-%m-%d %H:%M:%S"),
        )


class LeakageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leakage
        fields = (
            'id',
            'keyword',
            'fragment',
            'html_url',
            'file_name',
            'repo_name',
            'repo_url',
            'user_avatar',
            'user_name',
            'user_url',
            'leakage_status',
            'create_time'
        )

    def to_representation(self, instance):
        result = super().to_representation(instance)
        task = TaskSerializer(instance.task)
        result['task'] = task.data
        return result
