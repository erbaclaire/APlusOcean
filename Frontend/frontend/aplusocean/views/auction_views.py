from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
from django.conf import settings
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter
from django.views.decorators.csrf import csrf_exempt
import pika
import aplusocean.config as config
import pickle
import threading

def auctions(request):
    if request.method == 'GET':
        return render(request, 'aplusocean/auctions.html')

@csrf_exempt
def make_bid(request):
    if request.method == 'POST':
        account_id = request.GET.get('account_id')
        amount = request.POST.get('amount')
        data = {"account_id":account_id, "amount":amount, }
        response_json = DataLoader(settings.AUCTIONS_SERVICE, '/make_bid/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id=' + account_id)
        else:
            return HttpResponseRedirect('/error')

@csrf_exempt
def auction_details(request):
    if request.method == 'GET':
        item_id = request.GET.get('item')
        item = {"item_id": item_id}
        items_data = DataLoader(settings.ITEMS_SERVICE, '/get_item/').get_with_data_and_images(json.dumps(item))
        items_data = TimeFormatter(items_data).get_formatted_time()
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account_id = request.GET.get('account_id')
        account_data = requests.get('http://localhost:8083/all_users/')
        account_user = requests.get('http://localhost:8083/account_info/', data=json.dumps({'account_id': request.GET.get('account_id')}))
        bids_data = requests.get('http://localhost:8084/highest_bid/', data=json.dumps({'item_id':item_id}))
        seller_email = None
        for item in items_data:
            for account in json.loads(account_data.text):
                if item['fields']['account_id'] == account['pk']:
                    seller_email = account['fields']['email']
        next_bid = None
        highest_bid = None
        for bid in json.loads(bids_data.text):
            next_bid = bid['fields']['bid_amount']+1
            highest_bid = bid['fields']['bid_amount']
        data = {
            'items': items_data,
            'categories': category_data,
            'account_id': account_id,
            'accounts': json.loads(account_data.text),
            'account_user':json.loads(account_user.text),
            'highest_bid': highest_bid,
            'seller_email': seller_email,
            'next_bid': next_bid
        }
        return render(request, 'aplusocean/auction_details.html', data)

@csrf_exempt
def place_bid(request):
    print(request.method)
    if request.method == 'POST':
        buyer_account_id = request.GET.get('buyer_account_id')
        buyer_email = request.GET.get('buyer_email')
        seller_account_id = request.GET.get('seller_account_id')
        seller_email = request.GET.get('seller_email')
        item_id = request.GET.get('item_id')
        item_name = request.GET.get('item_name')
        bid = request.POST.get('amount')
        data = {'buyer_account_id':buyer_account_id, 'buyer_email':buyer_email, 'seller_account_id':seller_account_id, 'seller_email':seller_email, 'item_id':item_id, 'bid': bid, 'item_name':item_name}
        response = requests.post('http://localhost:8080/place_bid/', data=json.dumps(data))
        # print(response)
        # start_thread(data)
        item_data = requests.post('http://localhost:8080/has_bids/', data=json.dumps({'item_id':item_id}))
        return HttpResponseRedirect('/accounts/?account_id=' + buyer_account_id)
    return HttpResponseRedirect('/error/')

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
