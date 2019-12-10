from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Carts, Transactions
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import datetime
import pika

def index(request):
    return HttpResponse("Carts index page.")

@csrf_exempt
def all_carts(request):
    if request.method == 'GET':
        cart_items = serializers.serialize('json', Carts.objects.all())
        return HttpResponse(cart_items)

@csrf_exempt
def get_cart(request):
    if request.method == 'GET':
    	body_unicode = request.body.decode('utf-8')
    	body = json.loads(body_unicode)
    	account_id = body["account_id"]
    	cart_items = serializers.serialize('json', Carts.objects.filter(account_id=account_id))
    	return HttpResponse(cart_items)

@csrf_exempt
def get_cart_item(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cart_item_id = body["cart_item_id"]
        cart_item = serializers.serialize('json', Carts.objects.filter(cart_item_id=cart_item_id))
        return HttpResponse(cart_item)

@csrf_exempt
def add_item_to_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        item_id = body["item_id"]
        account_id = body["account_id"]
        price = body["price"]
        cart = Carts(item_id=item_id, account_id=account_id, price=price)
        cart.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def log_transaction(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # save transaction
        cart_item_id = body['cart_item_id']
        fname = body['fname']
        lname = body['lname']
        cardno = body['cardno']
        scode = body['scode']
        exdate = body['exdate']
        adr = body['adr']
        city = body['city']
        state = body['state']
        zip = body['zip']
        invoice = Transactions(cart_item_id=Carts(cart_item_id=cart_item_id), fname=fname, lname=lname, cardno=cardno, scode=scode,
	    	                   exdate=exdate, adr=adr, city=city, state=state, zip=zip)
        print(invoice)
        invoice.save()
        order_id = invoice.invoice_number
        cart_item = Carts.objects.get(cart_item_id=cart_item_id)
        # changed checked out status
        cart_item.checked_out = True
        cart_item.save()
        return HttpResponse(json.dumps({"status": "ok", "order_id": order_id}), content_type='application/json')

@csrf_exempt
def remove_bids_on_item_in_cart(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
        data = {'item_id':body["item_id"]}
        channel = connection.channel()
        channel.exchange_declare(exchange='remove_invalid_bids', exchange_type='topic')
        channel.basic_publish(exchange='remove_invalid_bids', routing_key='remove_invalid_bids', body=pickle.dumps(data))
        print(" [x] Sent %r" % "MESSAGE SENT", flush=True)
        connection.close()
