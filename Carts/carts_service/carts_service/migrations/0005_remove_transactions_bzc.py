# Generated by Django 2.2.7 on 2019-11-17 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts_service', '0004_auto_20191117_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='bzc',
        ),
    ]
