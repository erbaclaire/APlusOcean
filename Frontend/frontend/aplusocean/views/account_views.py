from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter

@csrf_exempt
def user_account(request):
    if request.method == "GET":
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        items_data = DataLoader(settings.ITEMS_SERVICE, '/view_inventory/').get_data_with_images()
        items_data = TimeFormatter(items_data).get_formatted_time()
        account = {'account_id': request.GET.get('account_id')}
        account_data = requests.get('http://localhost:8083/account_info/', data=json.dumps(account))
        watchlist_data = requests.get('http://localhost:8083/get_watchlist_items/', data=json.dumps({'account_id':request.GET.get('account_id')}))
        carts_data = requests.get(settings.CART_SERVICE+'/get_cart/', data=json.dumps({'account_id':request.GET.get('account_id')}))
        carts = json.loads(carts_data.text)
        bids_data = requests.get('http://localhost:8084/all_active_bids/', data=json.dumps({'account_id':request.GET.get('account_id')}))
        bids = json.loads(bids_data.text)
        # this is to prevent users from deleting/suspending their accounts if they have active cart items
        # if their items are in another's cart, if they have active bids, or they have auctions open with
        # active bids.
        # still need to add functionality to prevent account deletion if account has active bids
        has_outstanding_cart = False
        for cart in carts:
            if not cart["fields"]["checked_out"]:
                has_outstanding_cart = True
        any_items_have_bids = False
        for item in items_data:
            if item['fields']['has_bids'] and item['fields']['auction_live_now'] == True:
                any_items_have_bids = True
            if item['fields']['in_cart']:
                has_outstanding_cart = True
        has_highest_bid = False
        for bid in bids:
            for item in items_data:
                if bid['fields']['highest_bid'] == True and bid['fields']['item_id'] == item['pk'] and item['fields']['auction_live_now'] == True:
                    has_highest_bid = True
        data = {
            'items': items_data,
            'categories': category_data,
            'account': json.loads(account_data.text),
            'watchlist_items': json.loads(watchlist_data.text),
            'carts': json.loads(carts_data.text),
            'has_outstanding_cart': has_outstanding_cart,
            'any_items_have_bids': any_items_have_bids,
            'bids': bids,
            'has_highest_bid': has_highest_bid
        }
        # print(data)
        return render(request, 'aplusocean/user_account.html', data)
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def update_account(request):
    if request.method == "GET":
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account = {'account_id': request.GET.get('account_id')}
        account_data = requests.get('http://localhost:8083/account_info/', data=json.dumps(account))
        data = {
            'categories': category_data,
            'account': json.loads(account_data.text)
        }
        return render(request, 'aplusocean/account_updates.html', data)
    if request.method == "POST":
        account_id = request.POST.get('account_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        credit_card = request.POST.get('credit_card')
        cvv = request.POST.get('cvv')
        exdate = request.POST.get('exdate')
        adr = request.POST.get('adr')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        data = {"account_id":account_id, "fname":fname, "lname":lname, "email":email, "password":password, "credit_card":credit_card,
               "cvv":cvv, "exdate":exdate, "adr":adr, "city":city, "state":state, "zip":zip}
        accounts_response = requests.post('http://localhost:8083/update_account/', data=json.dumps(data))
        accounts_response_json = accounts_response.json()
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def suspend(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        account = {'account_id': account_id}
        accounts_response = requests.post('http://localhost:8083/suspend_account/', data=json.dumps(account))
        accounts_response_json = accounts_response.json()
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def un_suspend(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        account = {'account_id': request.GET.get('account_id')}
        accounts_response = requests.post('http://localhost:8083/un_suspend_account/', data=json.dumps(account))
        accounts_response_json = accounts_response.json()
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def delete(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        account = {'account_id': request.GET.get('account_id')}
        accounts_response = requests.post('http://localhost:8083/delete_account/', data=json.dumps(account))
        accounts_response_json = accounts_response.json()
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def watchlist_add(request):
    if request.method == 'POST':
        account_id = request.GET.get('account_id')
        desired_item = request.POST.get('desired_item')
        desired_price = float(request.POST.get('desired_price'))
        data = {'account_id':account_id, 'desired_item':desired_item, 'desired_price':desired_price}
        accounts_response = requests.post('http://localhost:8083/add_watchlist_item/', data=json.dumps(data))
        accounts_response = json.loads(accounts_response.text)
        if accounts_response["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')


@csrf_exempt
def watchlist_remove(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        item_id = request.POST.get('pk')
        data = {'item_id': item_id}
        accounts_response = DataLoader(settings.ACCOUNTS_SERVICE, '/watchlist_remove/').post_data(json.dumps(data))
        return HttpResponseRedirect('/accounts/?account_id=' + account_id)
    else:
        return HttpResponseRedirect('/error')
