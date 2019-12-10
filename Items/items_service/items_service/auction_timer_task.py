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
from django.core import serializers
import items_service.config as config

# Declare dictionary to keep track of which auctions have reached the time X minutes before the auction ends set by seller
auctions_sent_notif = set()

print("STARTING AUCTION TIMER TASK", flush=True)

# Compare auction start time and end time to current time to set auction_live_now variable - which has implications for what users can see
def check_time():
    for item in Items.objects.all():
        if item.auction_start_time != None and item.admin_stopped_auction == False and item.in_cart == False and item.sold == False and datetime.datetime.now() <= datetime.datetime.strptime(str(item.auction_end_time)[:-9], '%Y-%m-%d %H:%M'):
            starting_thread(item.auction_start_time, item.item_id)
        if item.auction_end_time != None and item.admin_stopped_auction == False and item.in_cart == False and item.sold == False:
            ending_thread(item.auction_end_time, item.item_id)

def starting_thread(start_time, item_id):
    target_function = start_time_delay
    thread = threading.Thread(target=target_function, args=(start_time, item_id,))
    thread.start()

def start_time_delay(start_time, item_id):
    startTime = datetime.datetime.strptime(str(start_time)[:-9], '%Y-%m-%d %H:%M')
    now = datetime.datetime.now()
    if now < startTime:
        pass
    else:
        item = Items.objects.get(item_id=item_id)
        if item.auction_live_now == False:
            item.auction_live_now = True
            item.save()
            print(str(item_id) + "-" + item.item_name + " auction has started; now: " + str(now) + "; auction_start_time: " + str(startTime))

def ending_thread(end_time, item_id):
    target_function = end_time_delay
    thread = threading.Thread(target=target_function, args=(end_time, item_id,))
    thread.start()

def end_time_delay(end_time, item_id):
    endTime = datetime.datetime.strptime(str(end_time)[:-9], '%Y-%m-%d %H:%M')
    now = datetime.datetime.now()
    item = Items.objects.get(item_id=item_id)
    # Send notification to bidders X minutes before end of auction - async message to Notifications microservice
    if now < endTime and item.auction_live_now == True:
        if item.auction_end_notif_time == None:
            auction_end_notif_time = 30
        else:
            auction_end_notif_time = item.auction_end_notif_time
        if (endTime - now) <= datetime.timedelta(minutes=auction_end_notif_time) and item_id not in auctions_sent_notif:
            # Send note to Bids to tell Bids that it needs to coral the information of all users who have placed bids on an auction
            # so that notifications can be sent out to all of those bidders
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
            channel = connection.channel()
            channel.exchange_declare(exchange='auction_ending', exchange_type='topic')
            message = {"ending_auction": item_id}
            channel.basic_publish(exchange='auction_ending',routing_key='auction_ending',body=json.dumps(message))
            print(" [x] Sent %r" % str(message))
            connection.close()
            auctions_sent_notif.add(item_id)
            print(auctions_sent_notif, flush=True)
    else:
        if item.auction_live_now == True:
            item.auction_live_now = False
            item.save()
            print(str(item_id) + "-" + item.item_name + " auction is over; now: " + str(now) + "; auction_end_time: " + str(endTime))
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
            channel = connection.channel()
            channel.exchange_declare(exchange='auction_over', exchange_type='topic')
            message = {"auction_over": item_id, "shipping_cost": item.shipping_cost}
            channel.basic_publish(exchange='auction_over',routing_key='auction_over',body=json.dumps(message))
            print(" [x] Sent %r" % str(message))
            connection.close()

# run
schedule.every(15).seconds.do(check_time)

while True:
    schedule.run_pending()
    time.sleep(30)
