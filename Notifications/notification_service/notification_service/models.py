from django.db import models


# Create your models here.
class UserMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    date_sent = models.DateTimeField(auto_now_add=True)


class SupportMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    date_sent = models.DateTimeField(auto_now_add=True)
