# Generated by Django 2.2.6 on 2019-11-12 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0016_items_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='has_bids',
            field=models.BooleanField(default=False),
        ),
    ]