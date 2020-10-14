# Create your models here.
from django.db import models
from utils import valid_token
from utils.basemodel import TimestampMixin, BasicMethodMixin
from utils.redistool import RS


class Task(TimestampMixin, BasicMethodMixin):
    user_id = models.CharField(max_length=10, help_text='用户ID')
    name = models.CharField(max_length=128, help_text='任务名称')
    keyword = models.CharField(max_length=128, help_text='关键词')
    first_search_time = models.DateTimeField(auto_now_add=True)
    next_search_time = models.DateTimeField(auto_now=True)
    finished_time = models.DateTimeField(auto_now=True)
    mail = models.TextField(null=True, default='', help_text='通知邮箱列表')
    ignore_org = models.TextField(null=True, default='', verbose_name='忽略指定组织或账号下的代码')
    ignore_repo = models.TextField(null=True, default='', verbose_name='忽略某类仓库下的代码, 如 github.io')


class Leakage(TimestampMixin, BasicMethodMixin):
    statusChoiceItem = (
        (0, '未处理'),
        (1, '已处理'),
        (2, '白名单')
    )
    user_id = models.CharField(max_length=10, help_text='用户ID')
    keyword = models.CharField(max_length=128, help_text='关键字名称', db_index=True)
    sha = models.CharField(max_length=128, help_text='文件hash值')
    fragment = models.TextField(null=False, help_text='结果详情')
    html_url = models.CharField(max_length=2048, help_text='结果地址')
    file_name = models.CharField(max_length=128, help_text='所在文件名')
    repo_name = models.CharField(max_length=128, help_text='仓库名')
    repo_url = models.CharField(max_length=128, help_text='仓库地址')
    user_avatar = models.CharField(max_length=128, help_text='用户头像')
    user_name = models.CharField(max_length=128, help_text='用户名')
    user_url = models.CharField(max_length=128, help_text='用户地址')
    hash_value = models.CharField(max_length=64, db_index=True, help_text='hash值')
    leakage_status = models.IntegerField(choices=statusChoiceItem, default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time']


class Token(TimestampMixin, BasicMethodMixin):
    user_id = models.CharField(max_length=10, help_text='用户ID')
    token = models.CharField(max_length=40, validators=[valid_token])

    def save(self, *args, **kwargs):
        rs_key = 'token:%s' % self.token
        RS.hset(rs_key, 'reset', '')
        return super(Token, self).save(*args, **kwargs)
