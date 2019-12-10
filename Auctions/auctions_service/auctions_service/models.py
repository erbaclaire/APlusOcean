from djongo import models
from django.utils import timezone

# Create Auction
class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    bid_amount = models.FloatField(null=False, default=0)
    seller_account_id = models.IntegerField(null=False, default=0)
    seller_email = models.CharField(max_length=150)
    buyer_account_id = models.IntegerField(null=False, default=0)
    buyer_email = models.CharField(max_length=150)
    item_id = models.IntegerField(null=False, default=0)
    item_name = models.CharField(max_length=200)
    highest_bid = models.BooleanField(default=False)
    most_current_bid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
