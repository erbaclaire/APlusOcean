from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
import json
from django.views.decorators.csrf import csrf_exempt
# use this to assure login before accessing page
from django.contrib.auth.decorators import login_required

# logic for when user goes to home page
def home(request):
    return render(request, 'aplusocean/index.html')

def error(request):
    return render(request, 'aplusocean/error.html')
