# Generated by Django 2.2.2 on 2019-10-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='ignore_org',
            field=models.TextField(default='', null=True, verbose_name='忽略指定组织或账号下的代码'),
        ),
        migrations.AddField(
            model_name='task',
            name='ignore_repo',
            field=models.TextField(default='', null=True, verbose_name='忽略某类仓库下的代码, 如 github.io'),
        ),
    ]