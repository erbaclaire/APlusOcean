# Generated by Django 2.2.6 on 2019-11-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0014_delete_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.TextField()),
            ],
        ),
    ]