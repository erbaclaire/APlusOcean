from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pika
import json
from .models import Bids
from django.core import serializers

def index(request):

    return HttpResponse("Auctions index page.")

@csrf_exempt
def highest_bid(request):
	if request.method == 'GET':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		item_id = body["item_id"]
		highest_bid = serializers.serialize('json', Bids.objects.filter(item_id=item_id, highest_bid=True))
		return HttpResponse(highest_bid)

@csrf_exempt
def all_active_bids(request):
	if request.method == 'GET':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		account_id = body["account_id"]
		all_bids = serializers.serialize('json', Bids.objects.filter(buyer_account_id=account_id))
		return HttpResponse(all_bids)

@csrf_exempt
def all_highest_bids(request):
	if request.method == 'GET':
		all_bids = serializers.serialize('json', Bids.objects.filter(highest_bid=True))
		return HttpResponse(all_bids)

@csrf_exempt
def all_bids(request):
	if request.method == 'GET':
		all_bids = serializers.serialize('json', Bids.objects.all())
		return HttpResponse(all_bids)