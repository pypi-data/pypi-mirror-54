# Generated by Django 2.1.5 on 2019-01-09 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider_filets', '0008_auto_20181121_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='textfilet',
            name='push',
            field=models.BooleanField(blank=True, default=False, help_text='Improve ranking of this content.'),
        ),
    ]
