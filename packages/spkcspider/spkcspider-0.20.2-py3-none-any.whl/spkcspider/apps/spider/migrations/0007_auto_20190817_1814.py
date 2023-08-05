# Generated by Django 2.2.4 on 2019-08-17 18:14

from django.db import migrations

from spkcspider.constants import ProtectionStateType


def forward(apps, schema_editor):
    AssignedProtection = apps.get_model("spider_base", "AssignedProtection")

    for i in AssignedProtection.objects.all():
        if i.active and i.instant_fail:
            i.state = ProtectionStateType.instant_fail
        elif i.active:
            i.state = ProtectionStateType.enabled
        else:
            i.state = ProtectionStateType.disabled
        i.save(update_fields=["state"])


def backward(apps, schema_editor):
    AssignedProtection = apps.get_model("spider_base", "AssignedProtection")

    for i in AssignedProtection.objects.all():
        if i.state == ProtectionStateType.instant_fail:
            i.active = True
            i.instant_fail = True
        elif i.state == ProtectionStateType.enabled:
            i.active = True
            i.instant_fail = False
        else:
            i.active = False
            i.instant_fail = False
        i.save(update_fields=["active", "instant_fail"])


class Migration(migrations.Migration):

    dependencies = [
        ('spider_base', '0006_auto_20190817_1814'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
