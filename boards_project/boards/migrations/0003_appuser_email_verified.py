# Generated by Django 2.2.4 on 2019-09-19 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20190820_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
