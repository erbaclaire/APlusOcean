import sys
sys.path.append("/items_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'items_service.settings')
import django
django.setup()
from items_service.models import Items, Categories
import datetime
import threading
import schedule
import time
import pika
import json
import items_service.config as config


def create_rpc_queue():
    print("CREATING RPC THREAD",flush=True)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.RABBIT_HOST))

    channel = connection.channel()

    channel.queue_declare(queue='rpc_delete_account_queue')

    def delete_associated_items(account_id):
        print("received account ID: " + str(account_id), flush=True)
        delete_items = Items.objects.filter(account_id=account_id).delete()
        return "success"

    def on_request(ch, method, props, body):
        account_id = body

        print(" [.] delete_account_items_for_id(%s)" % account_id, flush=True)
        response = delete_associated_items(account_id)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_delete_account_queue', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests", flush=True)
    channel.start_consuming()


create_rpc_queue()
