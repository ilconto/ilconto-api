# Generated by Django 2.2.4 on 2019-08-20 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardmember',
            old_name='boards',
            new_name='board',
        ),
    ]