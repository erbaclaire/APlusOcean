import sys
sys.path.append("/carts_service")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carts_service.settings')
import django
django.setup()
from carts_service.models import Carts, Transactions
import datetime
import threading
import schedule
import time
import carts_service.config as config
import requests
import json 

# Compare auction start time and end time to current time to set auction_live_now variable - which has implications for what users can see
def check_time():
    for cart in Carts.objects.all():
        if not cart.checked_out:
            in_cart_time = datetime.datetime.strptime(str(cart.in_cart_time)[:-13], '%Y-%m-%d %H:%M:%S')
            starting_thread(cart.cart_item_id, cart.account_id, cart.item_id, in_cart_time)

def starting_thread(cart_item_id, account_id, item_id, in_cart_time):
    target_function = start_time_delay
    thread = threading.Thread(target=target_function, args=(account_id, item_id, cart_item_id, in_cart_time))
    thread.start()

def start_time_delay(cart_item_id, account_id, item_id, in_cart_time):
    print("Starting cart time delay thread")
    now = datetime.datetime.now()
    print(in_cart_time)
    print(now)
    if (now-in_cart_time) >= datetime.timedelta(minutes=5):
        account = {'account_id': account_id}
        
        account_data = requests.get('http://0.0.0.0:8083/account_info/', data=json.dumps(account))
        account = json.loads(account_data.text)
        transaction = Transactions(cart_item_id=Carts(cart_item_id=cart_item_id), fname=account['fields']['first_name'], lname=account['fields']['last_name'], cardno=account['fields']['credit_number'],
                                   scode=account['fields']['credit_cvv'], exdate=account['fields']['exdate'], adr=account['fields']['address_street'], city=account['fields']['address_city'],
                                   state=account['fields']['address_state'], zip=account['fields']['address_zip'])
        transaction.save()
        cart = Carts.objects.filter(cart_item_id=cart_item_id)
        cart.checked_out = True
        cart.save()
        item = {'item_id':item_id, 'account_id':account_id}
        items_response_json = DataLoader('http://localhost:8080/item_sold/').post_data(json.dumps(item))
        print("automatic checkout")

# run
schedule.every(1).seconds.do(check_time)

while True:
    schedule.run_pending()
    time.sleep(5)

