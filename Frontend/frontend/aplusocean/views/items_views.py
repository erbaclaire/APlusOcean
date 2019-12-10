from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
from django.views.decorators.csrf import csrf_exempt
# use this to assure login before accessing page
from django.contrib.auth.decorators import login_required
import datetime
import base64
import pickle
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings as djangoSettings
import pytz
from django.conf import settings
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter

timezone = pytz.timezone("America/Chicago")


@csrf_exempt
def items(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        items_data = DataLoader(settings.ITEMS_SERVICE, '/view_inventory/').get_data_with_images()
        items_data = TimeFormatter(items_data).get_formatted_time()
        account_id = request.GET.get('account_id')
        account_data = requests.get('http://localhost:8083/all_users/')
        bids_data = requests.get('http://localhost:8084/all_highest_bids/')
        ok = False
        for user in json.loads(account_data.text):
            if account_id != None:
                if user['pk'] == int(account_id) and user['fields']['is_active'] == True and user['fields']['is_blocked'] == False:
                    ok = True
        data = {
            'items': items_data,
            'categories': category_data,
            'account_id': account_id,
            'accounts': json.loads(account_data.text),
            'bids': json.loads(bids_data.text),
            'ok': ok
        }
        return render(request, 'aplusocean/items.html', data)


@csrf_exempt
def new_items(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account_id = request.GET.get('account_id')
        data = {
            'categories': category_data,
            'account_id': account_id
        }
        return render(request, 'aplusocean/new_items.html', data)
    elif request.method == 'POST':
        account_id = request.GET.get('account_id')
        item_name = request.POST.get('item_name')
        item_pic = request.FILES['item_pic']
        path = default_storage.save('pic.png', ContentFile(item_pic.read()))
        with open(path, "rb") as imageFile:
            image = base64.encodebytes(imageFile.read())
            image_data = image.decode('ascii')
        imageFile.close()
        category_id = request.POST.get('category')
        print(category_id)
        category_id2 = request.POST.get('category2')
        if category_id2 != "":
            category_id = category_id2
        item_desc = request.POST.get('item_desc')
        quantity = request.POST.get('quantity')
        start_price = request.POST.get('start_price')
        shipping_cost = request.POST.get('shipping_cost')
        auction_start_time = request.POST.get('auction_start_time')
        auction_end_time = request.POST.get('auction_end_time')
        auction_end_notif_time = request.POST.get('auction_end_notif_time')
        buy_now = request.POST.get('buy_now')
        buy_now_price = request.POST.get('buy_now_price')
        data = {"account_id":account_id, "item_name": item_name, "item_pic": image_data, "category_id": category_id, "item_desc": item_desc,
                "quantity": quantity, "start_price": start_price, "shipping_cost": shipping_cost, "auction_start_time": auction_start_time,
                "auction_end_time": auction_end_time, "auction_end_notif_time": auction_end_notif_time, "buy_now": buy_now, "buy_now_price":buy_now_price}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/add_item/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')


@csrf_exempt
def update_items(request):
    if request.method == 'GET':
        return edit_item(request)
    elif request.method == 'POST':
        return edit_item_submit(request)


def edit_item(request):
    item_id = request.GET.get('item', '')
    data = {"item_id": item_id}
    items_data = DataLoader(settings.ITEMS_SERVICE, '/get_item/').get_with_data_and_images(json.dumps(data))
    items_data = TimeFormatter(items_data).get_formatted_time()
    category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
    account_id = request.GET.get('account_id')
    data = {
        'items': items_data,
        'categories': category_data,
        'account_id': account_id
    }
    return render(request, 'aplusocean/item_updates.html', data)


def edit_item_submit(request):
    if request.POST.__contains__("update"):
        print('update')
        account_id = request.GET.get('account_id')
        item_id = request.POST.get('item_id')
        item_name = request.POST.get('item_name')
        if request.POST.get('item_pic2') != "":
            item_pic = request.FILES['item_pic2']
            path = default_storage.save('pic.png', ContentFile(item_pic.read()))
            with open(path, "rb") as imageFile:
                image = base64.encodebytes(imageFile.read())
                image_data = image.decode('ascii')
            imageFile.close()
        else:
            image_data = ""
        category_id = request.POST.get('category')
        category_id2 = request.POST.get('category2')
        if category_id2 != "":
            category_id = category_id2
        item_desc = request.POST.get('item_desc')
        quantity = request.POST.get('quantity')
        start_price = request.POST.get('start_price')
        shipping_cost = request.POST.get('shipping_cost')
        auction_start_time = request.POST.get('auction_start_time')
        auction_end_time = request.POST.get('auction_end_time')
        auction_end_notif_time = request.POST.get('auction_end_notif_time')
        buy_now = request.POST.get('buy_now')
        buy_now_price = request.POST.get('buy_now_price')
        data = {"item_id": item_id, "item_name": item_name, "item_pic": image_data, "category_id": category_id,
                "item_desc": item_desc, "quantity": quantity,
                "start_price": start_price, "shipping_cost": shipping_cost, "auction_start_time": auction_start_time,
                "auction_end_time": auction_end_time, "auction_end_notif_time": auction_end_notif_time,
                "buy_now": buy_now, "buy_now_price":buy_now_price}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/seller_item_update/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    elif request.POST.__contains__("delete"):
        print("delete")
        account_id = request.GET.get('account_id')
        item_id = request.POST.get('item_id')
        data = {"item_id": item_id}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/delete_item/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts/?account_id='+account_id)
        else:
            return HttpResponseRedirect('/error')
    elif request.POST.__contains__("admin_delete_item"):
        print("delete")
        admin_account_id = request.GET.get('admin_account_id')
        item_id = request.POST.get('item_id')
        data = {"item_id": item_id}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/delete_item/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        elif response_json["status"] == "ok":
            return HttpResponseRedirect('/accounts')
        else:
            return HttpResponseRedirect('/error')
    elif request.POST.__contains__("admin_stop_auction"):
        print("stop auction")
        admin_account_id = request.GET.get('admin_account_id')
        print(admin_account_id)
        item_id = request.POST.get('item_id')
        data = {"item_id": item_id}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/stop_auction/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')
    return HttpResponseRedirect('/error')


@csrf_exempt
def flag_item(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        account_id = request.POST.get('account_id')
        data = {"item_id": item_id}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/flag_item/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            if account_id != None:
                return HttpResponseRedirect('/items/?account_id='+account_id)
            else:
                return HttpResponseRedirect('/items/')
        else:
            return HttpResponseRedirect('/error')

@csrf_exempt
def search_results(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        item_desc = request.GET.get('item_desc', '')
        category_id = request.GET.get('category', '')
        data = {"item_desc": item_desc, "category_id": category_id}
        items_data = DataLoader(settings.ITEMS_SERVICE, '/get_search_results/').get_with_data_and_images(
            json.dumps(data))
        items_data = TimeFormatter(items_data).get_formatted_time()
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        account_data = requests.get('http://localhost:8083/all_users/')
        bids_data = requests.get('http://localhost:8084/all_highest_bids/')
        ok = False
        for user in json.loads(account_data.text):
            if account_id != None:
                if user['pk'] == int(account_id) and user['fields']['is_active'] == True and user['fields']['is_blocked'] == False:
                    ok = True
        data = {
            'items': items_data,
            'categories': category_data,
            'account_id': account_id,
            'accounts': json.loads(account_data.text),
            'bids': json.loads(bids_data.text),
            'ok': ok
        }
        return render(request, 'aplusocean/search_results.html', data)

@csrf_exempt
def admin_add_delete_update_category(request):
    admin_account_id = request.GET.get('admin_account_id')
    if request.POST.__contains__("admin_add"):
        category = request.POST.get('category')
        data = {"category": category}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/add_category/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')
    elif request.POST.__contains__("admin_delete"):
        category_id = request.POST.get('category_id')
        data = {"category_id": category_id}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/delete_category/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')
    elif request.POST.__contains__("admin_update"):
        category_id = request.POST.get('category_id')
        category = request.POST.get('category')
        data = {"category_id": category_id, "category": category}
        response_json = DataLoader(settings.ITEMS_SERVICE, '/update_category/').post_data(json.dumps(data))
        if response_json["status"] == "ok":
            return HttpResponseRedirect('/support/admin/?admin_account_id='+admin_account_id)
        else:
            return HttpResponseRedirect('/error')
