# Generated by Django 2.2.6 on 2019-11-05 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0004_auto_20191105_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='auction_id',
            field=models.IntegerField(null=True),
        ),
    ]
