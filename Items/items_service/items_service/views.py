from django.http import HttpResponse
from .models import Items, Categories
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import datetime
import pytz
from dateutil import tz
import pika
import items_service.config as config
import threading
import pickle
import requests
timezone = pytz.timezone("America/Chicago")
from_tz = tz.gettz('UTC')
to_tz = tz.gettz('America/Chicago')


def index(request):
    return HttpResponse('Items index page.')

@csrf_exempt
def view_inventory(request):
    if request.method == 'GET':
        items = serializers.serialize('json', Items.objects.all().order_by('auction_end_time'))
        return HttpResponse(items)

@csrf_exempt
def view_categories(request):
    if request.method == 'GET':
        categories = serializers.serialize('json', Categories.objects.all())
        return HttpResponse(categories)

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body['account_id']
        item_name = body['item_name']
        item_pic = body['item_pic']
        category_id = body['category_id']
        item_desc = body['item_desc']
        quantity = body['quantity']
        start_price = body['start_price']
        shipping_cost = body['shipping_cost']
        if body['auction_start_time'] != "":
            auction_start_time = (datetime.datetime.strptime(body['auction_start_time'], '%m/%d/%Y %I:%M %p')).replace(tzinfo=from_tz).astimezone(to_tz)
        else:
            auction_start_time = None
        if body['auction_end_time'] != "":
            auction_end_time = (datetime.datetime.strptime(body['auction_end_time'], '%m/%d/%Y %I:%M %p')).replace(tzinfo=from_tz).astimezone(to_tz)
        else:
            auction_end_time = None
        if body['auction_end_notif_time'] =="":
            auction_end_notif_time = None
        else:
            auction_end_notif_time = body['auction_end_notif_time']
        buy_now = body['buy_now']
        buy_now_price = body['buy_now_price']
        if buy_now_price == "":
            buy_now_price = None
        start_price = body['start_price']
        if start_price == "":
            start_price = None
        print(buy_now_price, start_price, flush=True)
        try:
            temp = int(category_id)
            item_entry = Items(account_id=account_id, item_name=item_name,
                               category_id=Categories(category_id=category_id), item_desc=item_desc, quantity=quantity,
                               start_price=start_price, shipping_cost=shipping_cost,
                               auction_start_time=auction_start_time,
                               auction_end_time=auction_end_time, auction_end_notif_time=auction_end_notif_time,
                               buy_now=buy_now, buy_now_price=buy_now_price, item_pic=item_pic)
            item_entry.save()
        except ValueError:
            if not category_id.isnumeric():
                category_entry = Categories(category=category_id)
                category_entry.save()
                category_id = category_entry.category_id
            item_entry = Items(account_id=account_id, item_name=item_name,
                               category_id=Categories(category_id=category_id), item_desc=item_desc, quantity=quantity,
                               start_price=start_price, shipping_cost=shipping_cost,
                               auction_start_time=auction_start_time,
                               auction_end_time=auction_end_time, auction_end_notif_time=auction_end_notif_time,
                               buy_now=buy_now, buy_now_price=buy_now_price, item_pic=item_pic)
            item_entry.save()

        message = {'item_name':item_name, 'start_price':start_price, 'buy_now_price':buy_now_price}
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='new_watchlist_item', exchange_type='topic')
        channel.basic_publish(exchange='new_watchlist_item', routing_key=item_name, body=pickle.dumps(message))
        print(" [x] Sent %r" % "ITEM SENT", flush=True)

        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')


@csrf_exempt
def get_item(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["item_id"]
        items = serializers.serialize('json', Items.objects.filter(item_id=id))
        return HttpResponse(items)

@csrf_exempt
def seller_item_update(request):
     if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item = Items.objects.get(item_id=body['item_id'])
        item.item_name = body['item_name']
        if body['item_pic'] != "":
            item.item_pic = body['item_pic']
        item.item_desc = body['item_desc']
        item.quantity = body['quantity']
        item.start_price = body['start_price']
        item.shipping_cost = body['shipping_cost']
        if body['auction_start_time'] != "":
            auction_start_time = (datetime.datetime.strptime(body['auction_start_time'], '%m/%d/%Y %I:%M %p')).replace(tzinfo=from_tz).astimezone(to_tz)
            item.auction_start_time = auction_start_time
        else:
            auction_start_time = None
        if body['auction_end_time'] != "":
            auction_end_time = (datetime.datetime.strptime(body['auction_end_time'], '%m/%d/%Y %I:%M %p')).replace(tzinfo=from_tz).astimezone(to_tz)
            item.auction_end_time = auction_end_time
        else:
            auction_end_time = None
        if body['auction_end_notif_time'] == "":
            auction_end_notif_time = None
        else:
            auction_end_notif_time = body['auction_end_notif_time']
            item.auction_end_notif_time = auction_end_notif_time
        item.buy_now = body['buy_now']
        buy_now_price = body['buy_now_price']
        if buy_now_price == "":
            buy_now_price = None
        item.buy_now_price = buy_now_price
        try:
            if isinstance(int(body['category_id']), int):
                item.category_id = Categories(category_id=body['category_id'])
        except:
            category_entry = Categories(category=body['category_id'])
            category_entry.save()
            category_id = category_entry.category_id
            item.category_id = Categories(category_id=category_id)
        item.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["item_id"]
        item = Items.objects.filter(item_id=id)
        item.delete()
        data = {'item_id':id}
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='remove_invalid_bids', exchange_type='topic')
        channel.basic_publish(exchange='remove_invalid_bids', routing_key='remove_invalid_bids', body=pickle.dumps(data))
        print(" [x] Sent %r" % "MESSAGE SENT", flush=True)
        connection.close()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

# On auctions page allow users to flag an item
@csrf_exempt
def flag_item(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["item_id"]
        item = Items.objects.get(item_id=id)
        item.flagged = True
        item.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def view_flagged_items(request):
    if request.method == 'GET':
        flagged_items = serializers.serialize('json', Items.objects.filter(flagged=True))
        return HttpResponse(flagged_items)

@csrf_exempt
def get_search_results(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_desc = body['item_desc']
        category_id = body['category_id']
        if category_id == "1" and item_desc != "":
            items = serializers.serialize('json', Items.objects.filter(item_name__contains=item_desc))
        elif category_id == "1":
            items = serializers.serialize('json', Items.objects.all())
        else:
            items = serializers.serialize('json', Items.objects.filter(item_name__contains=item_desc, category_id=category_id))
        return HttpResponse(items)

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        category_name = body["category"]
        category = Categories(category=category_name)
        category.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def delete_category(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["category_id"]
        Categories.objects.filter(category_id=int(id)).delete()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def update_category(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body["category_id"]
        category_name = body["category"]
        category = Categories(category_id=id)
        category.category = category_name
        category.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def in_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_id = body["item_id"]
        item = Items.objects.get(item_id=item_id)
        item.in_cart = True
        item.auction_live_now = False
        item.in_whose_cart = body["account_id"]
        item.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def item_sold(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_id = body["item_id"]
        account_id = body["account_id"]
        item = Items.objects.get(item_id=item_id)
        item.in_cart = False
        item.cart_account_id = None
        item.sold = True
        item.sold_to_account_id = account_id
        item.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def stop_auction(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_id = body["item_id"]
        item = Items.objects.get(item_id=item_id)
        item.in_cart = False
        item.in_whose_cart = None
        item.auction_live_now = False
        item.admin_stopped_auction = True
        item.save()
        # write async message to Auctions so that all bids are deleted
        data = {'item_id':item_id}
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='remove_invalid_bids', exchange_type='topic')
        channel.basic_publish(exchange='remove_invalid_bids', routing_key='remove_invalid_bids', body=pickle.dumps(data))
        print(" [x] Sent %r" % "MESSAGE SENT", flush=True)
        connection.close()
        item_data = requests.post('http://localhost:8080/has_bids/', data=json.dumps({'item_id':item_id}))
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')


@csrf_exempt
def has_bids(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_id = body["item_id"]
        item = Items.objects.get(item_id=item_id)
        item.has_bids = True
        item.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

def send_pub_message(data):
    print("working")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='new_bid', exchange_type='topic')
    channel.basic_publish(exchange='new_bid', routing_key='new_bid', body=pickle.dumps(data))
    print(" [x] Sent %r" % "BID SENT", flush=True)
    connection.close()

def start_thread(data):
    # this is how you specify which function will be called when the thread starts
    target_function = send_pub_message
    # create thread with target function (specified above) and arguments for that target_functio
    thread = threading.Thread(target=target_function, args=(data,))
    # start the thread
    thread.start()

@csrf_exempt
def place_bid(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        start_thread(body)
