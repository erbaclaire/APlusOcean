import sys

sys.path.append("/auctions_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auctions_service.settings')
import django
django.setup()

import pika
import json
import pickle
from django.core import serializers
import auctions_service.config as config
from auctions_service.models import Bids
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
channel = connection.channel()
print(' [*] Waiting for messages about auctions over. To exit press CTRL+C', flush=True)
channel.exchange_declare(exchange='auction_over', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='auction_over', queue=queue_name, routing_key='auction_over')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body, flush=True)
    body = body.decode('utf-8')
    body_json = json.loads(body)
    print(body_json)
    data = Bids.objects.filter(item_id=body_json["auction_over"], highest_bid=True)
    data_json = serializers.serialize('json', data)
    readable_data = json.loads(data_json)
    print(data_json, flush=True)
    if readable_data:
        # THERE SHOULD ONLY BE ONE HIGHEST BID
        for bid in readable_data:
            price = float(body_json["shipping_cost"]) + float(bid["fields"]["bid_amount"])
            cart_data = {"item_id": bid["fields"]["item_id"], "account_id": bid["fields"]["buyer_account_id"], "price": price}
            channel.exchange_declare(exchange='cart_items', exchange_type='topic')
            channel.basic_publish(exchange='cart_items', routing_key='cart_items', body=pickle.dumps(cart_data))
            print("Sent item to cart")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
