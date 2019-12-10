from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import pytz
import threading
import schedule
import time
import datetime
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter
from django.conf import settings
import pika
import aplusocean.config as config
import pickle

timezone = pytz.timezone("America/Chicago")

@csrf_exempt
def cart(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        carts_data = DataLoader(settings.CART_SERVICE, '/get_cart/').get_with_data(json.dumps({"account_id": account_id}))
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        items_data = DataLoader(settings.ITEMS_SERVICE, '/view_inventory/').get_data_with_images()
        items_data = TimeFormatter(items_data).get_formatted_time()
        data = {
            'cart_items': carts_data,
            'items': items_data,
            'categories': category_data,
            'account_id': account_id
        }
        return render(request, 'aplusocean/carts.html', data)

@csrf_exempt
def buy_now(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        account_id = request.GET.get('account_id')
        price = float(request.POST.get('price')) + float(request.POST.get('shipping_cost'))
        data = {"item_id": item_id, "account_id": account_id, "price": price, "buy_now": True}
        carts_response_json = DataLoader(settings.CART_SERVICE, '/add_item_to_cart/').post_data(json.dumps(data))
        items_response_json = DataLoader(settings.ITEMS_SERVICE, '/in_cart/').post_data(json.dumps(data))
        if carts_response_json["status"] == "ok" and items_response_json["status"] == "ok":
            remove_bids_response_json = DataLoader(settings.CART_SERVICE, '/remove_bids_on_item_in_cart/').post_data(json.dumps(data))
            # connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
            # data = {'item_id':item_id}
            # channel = connection.channel()
            # channel.exchange_declare(exchange='remove_invalid_bids', exchange_type='topic')
            # channel.basic_publish(exchange='remove_invalid_bids', routing_key='remove_invalid_bids', body=pickle.dumps(data))
            # print(" [x] Sent %r" % "MESSAGE SENT", flush=True)
            # connection.close()
            return HttpResponseRedirect('/carts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')

@csrf_exempt
def checkout(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account_id = request.GET.get('account_id')
        account = {'account_id': request.GET.get('account_id')}
        account_data = requests.get('http://localhost:8083/account_info/', data=json.dumps(account))
        item_id = request.GET.get('item_id')
        item = {'item_id':item_id}
        item_data = DataLoader(settings.ITEMS_SERVICE, '/get_item/').get_with_data_and_images(json.dumps(item))
        cart_data = requests.get('http://localhost:8082/get_cart_item/', data=json.dumps({'cart_item_id':request.GET.get('cart_item_id')}))
        price = request.GET.get('price')
        data = {
            'categories': category_data,
            'account': json.loads(account_data.text),
            'account_id': account_id,
            'items': item_data,
            'cart_data': json.loads(cart_data.text),
            'price': price
        }
        return render(request, 'aplusocean/checkout.html', data)
    elif request.method == 'POST':
        # log transactions
        account_id = request.GET.get('account_id')
        cart_item_id = request.POST.get('cart_item_id')
        print(cart_item_id)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cardno = request.POST.get('cardno')
        scode = request.POST.get('scode')
        exdate = request.POST.get('exdate')
        adr = request.POST.get('adr')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        data = {"cart_item_id": cart_item_id, "fname": fname, "lname": lname, "cardno": cardno, "scode": scode,
                "exdate": exdate, "adr": adr, "city": city, "state": state, "zip": zip}
        carts_response_json = DataLoader(settings.CART_SERVICE, '/log_transaction/').post_data(json.dumps(data))
        # tell items that product is sold
        item_id = request.POST.get('item_id')
        item = {'item_id':item_id, 'account_id':account_id}
        items_response_json = DataLoader(settings.ITEMS_SERVICE, '/item_sold/').post_data(json.dumps(item))
        # rate seller
        seller_account_id = request.POST.get('seller_account_id')
        rating = request.POST.get('rating')
        accounts_response_json = json.loads(requests.post('http://localhost:8083/rate_seller/', data=json.dumps({'seller_rating':rating, 'seller_account_id':seller_account_id})).text)
        order_number = carts_response_json["order_id"]
        if carts_response_json["status"] == "ok" and items_response_json["status"] == "ok" and accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/confirmations?account_id='+account_id+'&confirmation='+str(order_number))
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')


@csrf_exempt
def order_confirmation(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        order_number = request.GET.get('confirmation')
        account = {'account_id': request.GET.get('account_id')}
        account_data = requests.get('http://localhost:8083/account_info/', data=json.dumps(account))
        data = {
            'orders': [{"order_number": order_number}],
            'account': json.loads(account_data.text)
        }
        return render(request, 'aplusocean/order_confirmation.html', data)
