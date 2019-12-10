# Generated by Django 2.2.6 on 2019-11-13 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportMessage',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]