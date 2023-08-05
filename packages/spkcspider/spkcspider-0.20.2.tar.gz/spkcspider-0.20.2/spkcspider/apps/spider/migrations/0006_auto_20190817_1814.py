# Generated by Django 2.2.4 on 2019-08-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider_base', '0005_auto_20190626_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedprotection',
            name='state',
            field=models.CharField(choices=[('a', 'disabled'), ('b', 'active'), ('c', 'instant_fail')], default='b', help_text='State of the protection.', max_length=1),
        ),
    ]
