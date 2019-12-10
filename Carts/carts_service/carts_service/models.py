from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create Carts
class Carts(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(null=False)
    item_id = models.IntegerField(null=False)
    price = models.FloatField(null=False) # price + shipping_costs
    in_cart_time = models.DateTimeField(default=timezone.now)
    checked_out = models.BooleanField(default=False)
    def __str__(self):
        return str(self.item_id)

# Create Transactions
class Transactions(models.Model):
	invoice_number = models.AutoField(primary_key=True)
	cart_item_id = models.ForeignKey(Carts, null=False, on_delete=models.CASCADE)
	fname = models.CharField(null=False, max_length=100)
	lname = models.CharField(null=False, max_length=100)
	cardno = models.CharField(null=False, max_length=16)
	scode = models.CharField(null=False, max_length=4)
	exdate = models.CharField(max_length=7, null=False)
	adr = models.CharField(null=False, max_length=100)
	city = models.CharField(null=False, max_length=100)
	state = models.CharField(null=False, max_length=20)
	zip = models.CharField(null=False, max_length=5)
