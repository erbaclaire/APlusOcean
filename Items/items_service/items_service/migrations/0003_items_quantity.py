# Generated by Django 2.2.6 on 2019-11-05 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0002_auto_20191105_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
    ]
