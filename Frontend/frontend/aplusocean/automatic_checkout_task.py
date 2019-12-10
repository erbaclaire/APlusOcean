import datetime
import threading
import schedule
import time
import requests
import json
import pytz

# automatic checkout after 5 minutes of an item in a cart
def check_cart_time():
    carts = requests.get('http://localhost:8082/all_carts/')
    carts = json.loads(carts.text)
    for cart in carts:
        if not cart['fields']['checked_out']:
            in_cart_time = datetime.datetime.strptime(str(cart['fields']['in_cart_time'])[:-8].replace('T', ' '), '%Y-%m-%d %H:%M')
            starting_thread(cart['pk'], cart['fields']['account_id'], cart['fields']['item_id'], in_cart_time)

def starting_thread(cart_item_id, account_id, item_id, in_cart_time):
    target_function = start_time_delay
    thread = threading.Thread(target=target_function, args=(cart_item_id, account_id, item_id, in_cart_time))
    thread.start()

def start_time_delay(cart_item_id, account_id, item_id, in_cart_time):
    now = datetime.datetime.now() + datetime.timedelta(hours=6)
    print(in_cart_time)
    print(now)
    if (now-in_cart_time) >= datetime.timedelta(minutes=5):
        account = {'account_id': account_id}
        account_data = requests.get('http://localhost:8083/account_info/', data=json.dumps(account))
        account = json.loads(account_data.text)
        for a in account:
            transaction_data = {'cart_item_id':cart_item_id, 'fname':a['fields']['first_name'], 'lname':a['fields']['last_name'], 'cardno':a['fields']['credit_number'],
                                'scode':a['fields']['credit_cvv'], 'exdate':a['fields']['exdate'], 'adr':a['fields']['address_street'], 'city':a['fields']['address_city'],
                                'state':a['fields']['address_state'], 'zip':a['fields']['address_zip']}
            checkout = requests.post('http://localhost:8082/log_transaction/', data=json.dumps(transaction_data))
            item = {'item_id':item_id, 'account_id':account_id}
            items_response_json = requests.post('http://localhost:8080/item_sold/', data=json.dumps(item))
            print("automatic checkout")

# run
schedule.every(30).seconds.do(check_cart_time)

while True:
    schedule.run_pending()
    time.sleep(1)
