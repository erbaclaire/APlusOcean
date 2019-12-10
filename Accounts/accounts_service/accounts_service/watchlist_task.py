import sys
sys.path.append("/accounts_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts_service.settings')
import django
django.setup()
from accounts_service.models import Accounts, Watchlists
import pika
import json
import pickle
import schedule
import time
import threading
from django.core import serializers
import accounts_service.config as config


def create_sub(item_topic):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
    channel = connection.channel()
    print(' [*] Waiting for messages about items that match watchlist items. To exit press CTRL+C', flush=True)
    channel.exchange_declare(exchange='new_watchlist_item', exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='new_watchlist_item', queue=queue_name, routing_key=item_topic)

    def callback(ch, method, properties, body):
        body = pickle.loads(body)
        print(" [x] Received %r" % body, flush=True)
        item_name = body['item_name']
        try:
            start_price = float(body['start_price'])
        except:
            start_price = -1
        try:
            buy_now_price = float(body['buy_now_price'])
        except:
            buy_now_price = -1
        watchers = serializers.serialize('json', Watchlists.objects.filter(desired_item__contains=item_name, desired_price__gte=start_price) | Watchlists.objects.filter(desired_item__contains=item_name, desired_price__gte=buy_now_price))
        watchers_json = json.loads(watchers)
        print("Watchers: ", flush=True)
        print(watchers, flush=True)
        for watcher in watchers_json:
            account = Accounts.objects.get(account_id=int(watcher["fields"]['account_id']))
            data = {"email":account.email, "type": "watchlist", "item":item_name}
            channel.basic_publish(exchange='notifications', routing_key='notifications', body=pickle.dumps(data))
            print("SENT NOTIFICATION", flush=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def start_topic_thread(item_topic):
    # this is how you specify which function will be called when the thread starts
    target_function = create_sub
    # create thread with target function (specified above) and arguments for that target_functio
    thread = threading.Thread(target=target_function, args=(item_topic,))
    # start the thread
    thread.start()

subs_created = set()

def check_items():
    watchlist_items = serializers.serialize('json', Watchlists.objects.all())
    watchlist = json.loads(watchlist_items)
    for item in watchlist:
        if item["fields"]["desired_item"] not in subs_created:
            start_topic_thread(item["fields"]["desired_item"])
            subs_created.add(item["fields"]["desired_item"])

schedule.every(30).seconds.do(check_items)

while True:
    schedule.run_pending()
    time.sleep(30)
