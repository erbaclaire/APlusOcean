# Generated by Django 2.2.6 on 2019-11-11 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0011_auto_20191111_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='category_id',
            field=models.ForeignKey(on_delete=models.SET(1), to='items_service.Categories'),
        ),
    ]