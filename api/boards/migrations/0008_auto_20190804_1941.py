# Generated by Django 2.2.3 on 2019-08-04 19:41

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_auto_20190804_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='scores',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict, null=True),
        ),
    ]
