# Generated by Django 2.2.4 on 2019-09-20 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_appuser_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_activated',
            field=models.BooleanField(default=True),
        ),
    ]
