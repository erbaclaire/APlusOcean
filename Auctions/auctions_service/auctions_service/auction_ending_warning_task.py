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



# fake_data = [
#     {
#      "bid_amount": 10,
#      "seller_account_id": 5,
#      "seller_email": "sarahkoop12@gmail.com",
#      "buyer_account_id": 3,
#      "buyer_email": "skoop@uchicago.edu",
#      "item_id": 203,
#      "item_name": "test",
#      "highest_bid": True},
#     {
#      "bid_amount": 6,
#      "seller_account_id": 5,
#      "seller_email": "sarahkoop12@gmail.com",
#      "buyer_account_id": 4,
#      "buyer_email": "skoop@alumni.nd.edu",
#      "item_id": 203,
#      "item_name": "test",
#      "highest_bid": False}
# ]
#
#
# def add_fake_data():
#     for item in fake_data:
#         bid = Bids(bid_amount=item["bid_amount"], seller_account_id=item["seller_account_id"],
#                    seller_email=item["seller_email"], buyer_account_id=item["buyer_account_id"],
#                    buyer_email=item["buyer_email"], item_id=item["item_id"], item_name=item["item_name"], highest_bid=item["highest_bid"])
#         bid.save()
#
#
# add_fake_data()

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
channel = connection.channel()
print(' [*] Waiting for messages about auctions about to expire. To exit press CTRL+C', flush=True)
channel.exchange_declare(exchange='auction_ending', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='auction_ending', queue=queue_name, routing_key='auction_ending')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body, flush=True)
    body = body.decode('utf-8')
    body_json = json.loads(body)
    print(body_json)
    print(body_json["ending_auction"])

    data = Bids.objects.filter(item_id=body_json["ending_auction"])
    data_json = serializers.serialize('json', data)
    readable_data = json.loads(data_json)
    print(data_json, flush=True)
    if readable_data:
        seller_data = readable_data[0]["fields"]["seller_email"]
        seller_item = readable_data[0]["fields"]["item_name"]
        notification_data = {"email": seller_data, "type": "auction_expiration_seller", "item": seller_item}
        channel.basic_publish(exchange='notifications', routing_key='notifications', body=pickle.dumps(notification_data))
        for bid in readable_data:
            notification_data = {"email": bid["fields"]["buyer_email"], "type": "auction_expiration", "item": bid["fields"]["item_name"]}
            channel.basic_publish(exchange='notifications', routing_key='notifications', body=pickle.dumps(notification_data))
        print("SENT NOTIFICATION", flush=True)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
