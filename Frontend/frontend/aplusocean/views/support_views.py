from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter
import datetime

@csrf_exempt
def support(request):
    if request.method == "GET":
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account_id = request.GET.get('account_id')
        data = {
            'categories': category_data,
            'account_id': account_id
        }
        return render(request, 'aplusocean/support.html', data)
    elif request.method == "POST":
        account_id = request.GET.get('account_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data = {"first_name": fname, "last_name": lname, "email": email, "message": message}
        response_json = DataLoader(settings.NOTIFICATION_SERVICE, '/complaints/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')

@csrf_exempt
def support_response(request):
    if request.method == "GET":
        admin_account_id = request.GET.get('admin_account_id')
        message_id = request.GET.get('message', '')
        data = {'message_id': message_id}
        message_data = DataLoader(settings.NOTIFICATION_SERVICE, '/complaints/').get_with_data(json.dumps(data))
        data = {
            'messages': message_data,
            'admin_account_id': admin_account_id
        }
        return render(request, 'aplusocean/support_message_response.html', data)
    if request.method == "POST":
        admin_account_id = request.GET.get('admin_account_id')
        message = request.POST.get('message')
        message_id = request.POST.get('message_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        data = {'message': message, 'email': email, 'message_id': message_id, 'first_name': first_name}
        response_json = DataLoader(settings.NOTIFICATION_SERVICE, '/complaints/admin/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')

@csrf_exempt
def admin_support(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        flagged_items_data = DataLoader(settings.ITEMS_SERVICE, '/view_flagged_items/').get_data_with_images()
        messages_data = DataLoader(settings.NOTIFICATION_SERVICE, '/complaints/').get_data()
        items_data = DataLoader(settings.ITEMS_SERVICE, '/view_inventory/').get_data()
        flagged_items_data = TimeFormatter(flagged_items_data).get_formatted_time()
        items_data = TimeFormatter(items_data).get_formatted_time()
        accounts_data = requests.get('http://localhost:8083/all_users/')
        accounts_data = json.loads(accounts_data.text)
        admin_account_id = request.GET.get('admin_account_id')
        current_time = datetime.datetime.now()
        bids_data = requests.get('http://localhost:8084/all_highest_bids/')
        bids_data = json.loads(bids_data.text)
        # this is to prevent an admin from deleting/blocking an accounts if the user has active cart items
        # if the user has items in another's cart, if the user has active bids, or the user has auctions open with
        # active bids.
        # still need to add functionality to prevent account deletion if account has active bids
        has_outstanding_cart = {}
        any_items_have_bids = {}
        has_highest_bid = {}
        for account in accounts_data:
            for item in items_data:
                if (account['pk'] == item['fields']['account_id'] and item['fields']['in_cart']) or (item['fields']['cart_account_id'] == account['pk']):
                    has_outstanding_cart[account['pk']] = True
                if account['pk'] == item['fields']['account_id'] and item['fields']['has_bids'] and item['fields']['auction_live_now'] == True:
                    any_items_have_bids[account['pk']] = True
            for bid in bids_data:
                for item in items_data:
                    if account['pk'] == bid['fields']['buyer_account_id'] and item['pk'] == bid['fields']['item_id'] and item['fields']['auction_live_now'] == True:
                        has_highest_bid[account['pk']] = True
        # auction metrics
        metrics_data = requests.get('http://localhost:8084/all_bids/')
        metrics_data= json.loads(metrics_data.text)
        highest = {'last_24_hours':0, 'last_week':0, 'last_month':0, 'last_year':0}
        avg = {'last_24_hours':0, 'last_week':0, 'last_month':0, 'last_year':0}
        count_24 = 1
        week_count = 1
        month_count = 1
        year_count = 1
        for md in metrics_data:
            for item in items_data:
                if item['fields']['auction_end_time'] != None:
                    ending_date = item['fields']['auction_end_time']
                    now = datetime.datetime.now()
                    highest_bid = md['fields']['highest_bid']
                    date_posted = datetime.datetime.strptime(str(md['fields']['date_posted']).replace("T"," ")[:-8], '%Y-%m-%d %H:%M')-datetime.timedelta(hours=6)
                    bid = md['fields']['bid_amount']
                    print(bid)
                    # highest bids in timeframe
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and  highest_bid == True and (now-date_posted) <= datetime.timedelta(hours=24) and bid >= highest['last_24_hours']:
                        highest['last_24_hours'] = bid
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and  highest_bid == True and (now-date_posted) <= datetime.timedelta(days=7) and bid >= highest['last_week']:
                        highest['last_week'] = bid
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and  highest_bid == True and (now-date_posted) <= datetime.timedelta(days=30) and bid >= highest['last_month']:
                        highest['last_month'] = bid
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and  highest_bid == True and (now-date_posted) <= datetime.timedelta(days=365) and bid >= highest['last_year']:
                        highest['last_year'] = bid
                    # avg bid
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and (now-date_posted) <= datetime.timedelta(hours=24):
                        count_24 += 1
                        avg['last_24_hours'] = (avg['last_24_hours'] + bid)
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and (now-date_posted) <= datetime.timedelta(days=7):
                        week_count += 1
                        avg['last_week'] = (avg['last_week'] + bid)
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and (now-date_posted) <= datetime.timedelta(days=30):
                        month_count += 1
                        avg['last_month'] = (avg['last_month'] + bid)
                    if item['pk'] == md['fields']['item_id'] and ending_date <= now and (now-date_posted) <= datetime.timedelta(days=365):
                        year_count += 1
                        avg['last_year'] = (avg['last_year'] + bid)
        avg['last_24_hours'] = avg['last_24_hours']/count_24
        avg['last_week'] = avg['last_week']/week_count
        avg['last_month'] = avg['last_month']/month_count
        avg['last_year'] = avg['last_year']/year_count
        data = {
                'categories': category_data,
                'flagged_items': flagged_items_data,
                'messages': messages_data,
                'items': items_data,
                'accounts': accounts_data,
                'admin_account_id': admin_account_id,
                'today': current_time,
                'has_outstanding_cart': has_outstanding_cart,
                'any_items_have_bids': any_items_have_bids,
                'has_highest_bid': has_highest_bid,
                'bids': bids_data,
                'highest': highest,
                'avg': avg
        }
        return render(request, 'aplusocean/admin_support.html', data)
    elif request.method == 'POST':
        admin_account_id = request.GET.get('admin_account_id')
        account = {'account_id': request.POST.get('account_id')}
        if request.POST.__contains__('block_user'):
            accounts_response = requests.post('http://localhost:8083/block_user/', data=json.dumps(account))
        elif request.POST.__contains__('un_block_user'):
            accounts_response = requests.post('http://localhost:8083/un_block_user/', data=json.dumps(account))
        elif request.POST.__contains__('remove_user'):
            print("REMOVING USER")
            print(account)
            accounts_response = requests.post('http://localhost:8083/delete_account/', data=json.dumps(account))
        accounts_response_json = accounts_response.json()
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')
