# Generated by Django 2.2.4 on 2019-09-20 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_appuser_activation_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 9, 20, 13, 2, 2, 972126)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='board',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 9, 20, 13, 2, 13, 878888)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='boardmember',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 9, 20, 13, 2, 47, 351992)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='boardmember',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]