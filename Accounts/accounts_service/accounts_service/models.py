from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create Account
class Accounts(models.Model):
    account_id = models.AutoField(primary_key = True)
    email = models.CharField(null=False, max_length=100)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    password = models.CharField(max_length=100, null=False)
    seller_rating = models.FloatField(null=True)
    number_of_ratings = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    credit_number = models.CharField(max_length=16, null=False)
    credit_cvv = models.IntegerField(null=False)
    exdate = models.CharField(max_length=7, null=False)
    address_street = models.CharField(max_length=100, null=False)
    address_city = models.CharField(max_length=100, null=False)
    address_state = models.CharField(max_length=100, null=False)
    address_zip = models.CharField(null=False, max_length=5)

class Watchlists(models.Model):
    watchlist_id = models.AutoField(primary_key = True)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=False)
    desired_item = models.CharField(max_length=100, null=False)
    desired_price = models.FloatField(null=True)
