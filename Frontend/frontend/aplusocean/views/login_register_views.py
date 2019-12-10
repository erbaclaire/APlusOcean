from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from aplusocean.classes.DataLoader import DataLoader
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from aplusocean.classes.DataLoader import DataLoader
from aplusocean.classes.TimeFormatter import TimeFormatter

@csrf_exempt
def login(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        data = {
            'categories': category_data
        }
        return render(request, 'aplusocean/login.html', data)
    elif request.method == 'POST':
        # Confirm login credentials
        email = request.POST.get('em')
        password = request.POST.get('pass')
        data = {"email":email, "password":password}
        accounts_response = requests.post('http://localhost:8083/account_info/', data=json.dumps(data))
        account = json.loads(accounts_response.text)
        for a in account:
            account_id = str(a['pk'])
        return HttpResponseRedirect('/accounts/?account_id='+account_id)
    else:
        return HttpResponseRedirect('/error')

@csrf_exempt
def register(request):
    if request.method == 'GET':
        category_data = DataLoader(settings.ITEMS_SERVICE, '/view_categories/').get_data()
        data = {
            'categories': category_data
        }
        return render(request, 'aplusocean/register.html', data)
    if request.method == 'POST':
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
        data = {"fname":fname, "lname":lname, "email":email, "password":password, "credit_card":credit_card,
               "cvv":cvv, "exdate":exdate, "adr":adr, "city":city, "state":state, "zip":zip}
        accounts_response = requests.post('http://localhost:8083/new_user/', data=json.dumps(data))
        accounts_response_json = accounts_response.json()
        print(accounts_response_json)
        if accounts_response_json["status"] == "ok":
            return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/error')
    else:
        return HttpResponseRedirect('/error')
