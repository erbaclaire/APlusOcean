# Generated by Django 2.2.7 on 2019-11-16 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='address_number',
        ),
    ]
