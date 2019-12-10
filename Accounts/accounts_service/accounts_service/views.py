from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Accounts, Watchlists
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib import messages
import json
import datetime
from django.conf import settings
from accounts_service.classes.DataLoader import DataLoader
from accounts_service.classes.TimeFormatter import TimeFormatter
from accounts_service.classes.DeleteAccountRpcClient import DeleteAccountRpcClient
import pika
import pickle
import threading
import accounts_service.config as config
import requests


def index(request):
    return HttpResponse('Accounts index page.')

@csrf_exempt
def account_info(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account = body["account_id"]
        account_info = serializers.serialize('json', Accounts.objects.filter(account_id=account))
        return HttpResponse(account_info)
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email_attempt = body['email']
        password_attempt = body['password']
        account = Accounts.objects.get(email=body['email'])
        account_json = serializers.serialize('json', Accounts.objects.filter(email=body['email']))
        if account.password == password_attempt:
            return HttpResponse(account_json)

@csrf_exempt
def all_users(request):
    if request.method == "GET":
        accounts = serializers.serialize('json', Accounts.objects.all())
        return HttpResponse(accounts)

@csrf_exempt
def new_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fname = body['fname']
        lname = body['lname']
        email = body['email']
        password = body['password']
        credit_card = body['credit_card']
        cvv = body['cvv']
        exdate = body['exdate']
        adr = body['adr']
        city = body['city']
        state = body['state']
        zip = body['zip']
        accounts = Accounts.objects.all()
        for account in accounts:
            if email == account.email:
                return HttpResponse(json.dumps({"status": "email already in use"}), content_type='application/json')
        account = Accounts(first_name=fname, last_name=lname, email=email, password=password,
                           credit_number=credit_card, credit_cvv=cvv, exdate=exdate, address_street=adr, address_city=city,
                           address_state=state, address_zip=zip)
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def update_account(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account = Accounts.objects.get(account_id=body['account_id'])
        account.first_name = body['fname']
        account.last_name = body['lname']
        account.email = body['email']
        account.password = body['password']
        account.credit_number = body['credit_card']
        account.credit_cvv = body['cvv']
        account.exdate = body['exdate']
        account.address_street = body['adr']
        account.address_city = body['city']
        account.address_state = body['state']
        account.address_zip = body['zip']
        accounts = Accounts.objects.all()
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def block_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account = Accounts.objects.get(account_id=body['account_id'])
        account.is_blocked = True
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def un_block_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account = Accounts.objects.get(account_id=body['account_id'])
        account.is_blocked = False
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def suspend_account(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body["account_id"]
        ### delete all items posted by user
        delete_account_rpc = DeleteAccountRpcClient()
        print(" [x] Requesting account deletion")
        response = delete_account_rpc.call(account_id)
        print(" [.] Got %r" % response)

        account = Accounts.objects.get(account_id=body['account_id'])
        account.is_active = False
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def un_suspend_account(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account = Accounts.objects.get(account_id=body['account_id'])
        account.is_active = True
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        print("RECEIVED REQUEST TO DLETE ACCOUNT", flush=True)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body["account_id"]
        delete_account_rpc = DeleteAccountRpcClient()
        print(" [x] Requesting account deletion", flush=True)
        response = delete_account_rpc.call(account_id)
        print(" [.] Got %r" % response, flush=True)

        Accounts.objects.get(account_id=body['account_id']).delete()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def add_watchlist_item(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body['account_id']
        desired_item = body['desired_item']
        desired_price = body['desired_price']
        watchlist_item = Watchlists(account_id=Accounts(account_id=account_id), desired_item=desired_item, desired_price=desired_price)
        watchlist_item.save()
        # start_topic_thread(desired_item)
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')

@csrf_exempt
def remove_watchlist_items(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Watchlists.objects.get(pk=body['item_id']).delete()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')


@csrf_exempt
def get_watchlist_items(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body['account_id']
        watchlist_items = serializers.serialize('json', Watchlists.objects.filter(account_id=account_id))
        print("Watchlist Items: ", flush=True)
        print(watchlist_items,flush=True)
        return HttpResponse(watchlist_items)

@csrf_exempt
def rate_seller(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        seller_rating = body['seller_rating']
        account_id = body['seller_account_id']
        account = Accounts.objects.get(account_id=account_id)
        account.number_of_ratings = account.number_of_ratings + 1
        account.save()
        if account.seller_rating != None:
            account.seller_rating = (account.seller_rating + float(seller_rating))/account.number_of_ratings
        else:
            account.seller_rating = (float(seller_rating))/account.number_of_ratings
        account.save()
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')
