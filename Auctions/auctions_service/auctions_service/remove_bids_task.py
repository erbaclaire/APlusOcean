import sys
sys.path.append("/auctions_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auctions_service.settings')
import django
django.setup()
from auctions_service.models import Bids
import pika
import json
import pickle
import auctions_service.config as config

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
channel = connection.channel()
channel.exchange_declare(exchange='remove_invalid_bids', exchange_type='topic')
result = channel.queue_declare('', exclusive=True)
queue_name=result.method.queue
channel.queue_bind(exchange='remove_invalid_bids',queue=queue_name, routing_key='remove_invalid_bids')

print(' [*] Waiting to remove bids that are no longer of interest/valid. To exit press CTRL+C')
def callback(ch, method, properties, body):
    body = pickle.loads(body)
    print(" [x] Received %r" % body)
    item_id = body['item_id']
    Bids.objects.filter(item_id=item_id).delete()

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()