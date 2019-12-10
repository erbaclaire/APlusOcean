from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create Categories lookup table
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.TextField()

    def __str__(self):
        return self.category

# Create Items table
class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(null=False)
    item_name = models.CharField(null=False, max_length=100)
    category_id = models.ForeignKey(Categories, on_delete=models.SET(1), default=1)
    item_pic = models.TextField(null=True)
    item_desc = models.TextField()
    quantity = models.IntegerField(null=False)
    start_price = models.FloatField(null=True)
    shipping_cost = models.FloatField(null=False)
    flagged = models.BooleanField(default=False)
    auction_start_time = models.DateTimeField(null=True, default=timezone.now)
    auction_end_time = models.DateTimeField(null=True, default=timezone.now)
    auction_end_notif_time = models.IntegerField(null=True)
    buy_now = models.BooleanField(default=False)
    buy_now_price = models.FloatField(null=True)
    auction_live_now = models.BooleanField(default=False)
    admin_stopped_auction = models.BooleanField(default=False)
    has_bids = models.BooleanField(default=False)
    in_cart = models.BooleanField(default=False)
    cart_account_id = models.IntegerField(null=True)
    sold = models.BooleanField(default=False)
    sold_to_account_id = models.IntegerField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.item_name
