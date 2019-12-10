import sys
sys.path.append("/carts_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carts_service.settings')
import django
django.setup()
from carts_service.models import Carts, Transactions
import datetime
import threading
import schedule
import time
import carts_service.config as config
import requests
import json
import pika
import pickle

# Compare auction start time and end time to current time to set auction_live_now variable - which has implications for what users can see
print("CARTS TASK STARTING", flush=True)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
channel = connection.channel()
print(' [*] Waiting for items to move to carts', flush=True)
channel.exchange_declare(exchange='cart_items', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='cart_items', queue=queue_name, routing_key='cart_items')

def callback(ch, method, properties, body):
    body = pickle.loads(body)
    print(" [x] Received %r" % body, flush=True)
    item_id = body["item_id"]
    account_id = body["account_id"]
    price = body["price"]
    cart = Carts(item_id=item_id, account_id=account_id, price=price)
    cart.save()

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
