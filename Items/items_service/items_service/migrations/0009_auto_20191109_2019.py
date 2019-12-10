# Generated by Django 2.2.6 on 2019-11-09 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_service', '0008_auto_20191106_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='in_auction',
            new_name='auction_exists',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='auction_id',
            new_name='sold_to_account_id',
        ),
        migrations.RemoveField(
            model_name='items',
            name='sold_to',
        ),
        migrations.AddField(
            model_name='items',
            name='auction_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='items',
            name='auction_live_now',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='items',
            name='auction_start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='items',
            name='buy_now',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='item_pic',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='items',
            name='shipping_cost',
            field=models.FloatField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='start_price',
            field=models.FloatField(default=False),
            preserve_default=False,
        ),
    ]
