# Generated by Django 2.1.5 on 2019-01-20 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spider_webcfg', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webconfig',
            name='creation_url',
        ),
        migrations.RemoveField(
            model_name='webconfig',
            name='token',
        ),
    ]
