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
channel.exchange_declare(exchange='new_bid', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='new_bid', queue=queue_name, routing_key="new_bid")

print(' [*] Waiting for new_bids. To exit press CTRL+C')
def callback(ch, method, properties, body):
    body = pickle.loads(body)
    print(" [x] Received %r" % body)
    bid = body['bid']
    seller_account_id = body['seller_account_id']
    seller_email = body['seller_email']
    buyer_account_id = body['buyer_account_id']
    buyer_email = body['buyer_email']
    item_id = body['item_id']
    item_name = body['item_name']
    other_bids = Bids.objects.filter(item_id=item_id)
    # make all other bids not highest bid
    # make all other bids for the account on this item not currentelse:
    try:
      highest_bid = Bids.objects.get(item_id=item_id, highest_bid=True)
      highest_bid = highest_bid.bid_amount
    except:
      highest_bid = None
    print(highest_bid, float(bid), flush=True)
    # not first bid
    if highest_bid != None:
      # outdated bid
      if float(bid) <= highest_bid:
        current_highest_bidder = None
        current_highest_bidder_email = None
        for obid in other_bids:
          account_value = obid.buyer_account_id
          if buyer_account_id == str(obid.buyer_account_id):
            obid.most_current_bid = False
            obid.save()
        bid = Bids(bid_amount=bid, seller_account_id=seller_account_id, seller_email=seller_email, buyer_account_id=buyer_account_id,
                   buyer_email=buyer_email, item_id=item_id, item_name=item_name, highest_bid=False, most_current_bid = True)
        bid.save()
        print(" [x] Bid placed - but it isn't the highest anymore")
        # tell user that they have already been outbid because there bids was too late
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        channel = connection.channel()
        # channel.queue_declare(queue='notifications', durable=True)
        channel.exchange_declare(exchange='notifications', exchange_type='topic')
        message = {'email':buyer_email, 'type':'higher_bid', 'bid':body['bid'], 'item':item_name}
        channel.basic_publish(exchange='notifications',routing_key='notifications',body=pickle.dumps(message))
        print(" [x] Sent %r" % str(message))
        connection.close()
      # valid bid
      else:
        current_highest_bidder = None
        current_highest_bidder_email = None
        for obid in other_bids:
          obid.highest_bid = False
          obid.save()
          if current_highest_bidder == None:
            current_highest_bidder = obid.pk
            current_highest_bidder_email = obid.buyer_email
          if obid.pk > current_highest_bidder:
            current_highest_bidder = obid.pk
            current_highest_bidder_email = obid.buyer_email
          account_value = obid.buyer_account_id
          if buyer_account_id == str(obid.buyer_account_id):
            obid.most_current_bid = False
            obid.save()
        # save bid
        bid = Bids(bid_amount=bid, seller_account_id=seller_account_id, seller_email=seller_email, buyer_account_id=buyer_account_id,
                   buyer_email=buyer_email, item_id=item_id, item_name=item_name, highest_bid=True, most_current_bid = True)
        bid.save()
        print(" [x] Bid placed")
        # send message to Notifications to allow notifying seller of new bid on their item
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='notifications', exchange_type='topic')
        message = {'email':seller_email, 'type':'seller_bid', 'bid':body['bid'], 'item':item_name}
        channel.basic_publish(exchange='notifications',routing_key='notifications',body=pickle.dumps(message))
        print(" [x] Sent %r" % str(message))
        connection.close()
        # send message to Notifications to allow last highest bidder of new higher on their item
        if current_highest_bidder != None:
          connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
          channel = connection.channel()
          # channel.queue_declare(queue='notifications', durable=True)
          channel.exchange_declare(exchange='notifications', exchange_type='topic')
          message = {'email':current_highest_bidder_email, 'type':'higher_bid', 'bid':body['bid'], 'item':item_name}
          channel.basic_publish(exchange='notifications',routing_key='notifications',body=pickle.dumps(message))
          print(" [x] Sent %r" % str(message))
          connection.close()
    # first bid
    else:
      # save bid
      bid = Bids(bid_amount=bid, seller_account_id=seller_account_id, seller_email=seller_email, buyer_account_id=buyer_account_id,
                 buyer_email=buyer_email, item_id=item_id, item_name=item_name, highest_bid=True, most_current_bid = True)
      bid.save()
      print(" [x] Bid placed")
      # send message to Notifications to allow notifying seller of new bid on their item
      connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
      channel = connection.channel()
      channel.exchange_declare(exchange='notifications', exchange_type='topic')
      message = {'email':seller_email, 'type':'seller_bid', 'bid':body['bid'], 'item':item_name}
      channel.basic_publish(exchange='notifications',routing_key='notifications',body=pickle.dumps(message))
      print(" [x] Sent %r" % str(message))
      connection.close()

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
