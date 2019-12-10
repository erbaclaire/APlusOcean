# import pika
# import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from notification_service.classes.EmailData import EmailData
from notification_service.classes.MessageText import MessageText
from notification_service.classes.UserComplaint import UserComplaint
from notification_service.models import SupportMessage
from django.core import serializers
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pika
import pickle
import notification_service.config as config


sg = SendGridAPIClient('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')

def send_notification(email, subject, message_html):
    message = Mail(
        from_email='notifications@aplusocean.com',
        to_emails=email,
        subject=subject,
        html_content=message_html)
    try:
        print("TRYING TO SEND EMAIL", flush=True)
        response = sg.send(message)
    except Exception as e:
        print("EXCEPTION SENDING EMAIL", flush=True)
        print(e,flush=True)
        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')
    if 200 <= int(response.status_code) < 300:
        return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')


def index(request):
    return HttpResponse("Notifications main index.")


@csrf_exempt
def notification(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print("RECEIVED BODY", flush=True)
        print(body, flush=True)
        email = body['email']
        type = body['type']
        message = MessageText(type, body)
        message_text = message.get_message_text()
        subject = message.get_message_subject()
        return send_notification(email, subject, message_text)





@csrf_exempt
def user_complaints(request):
    if request.method == 'GET':
        return get_user_complaints(request)
    elif request.method == 'POST':
        return add_user_complaint(request)


def get_user_complaints(request):
    complaints = []
    complaints_results = serializers.serialize('json', SupportMessage.objects.all().order_by('date_sent'))
    complaints_list =json.loads(complaints_results)
    for message in complaints_list:
        complaint = UserComplaint(message["pk"], message["fields"]["first_name"], message["fields"]["last_name"], message["fields"]["email"], message["fields"]["message"], message["fields"]["date_sent"])
        complaints.append(complaint.get_json())
    user_complaints = json.dumps(complaints)
    return HttpResponse(user_complaints, content_type='application/json')



def add_user_complaint(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    first_name = body['first_name']
    last_name = body['last_name']
    message = body['message']
    email = body['email']
    message = SupportMessage(first_name=first_name, last_name=last_name, email=email, message=message)
    message.save()
    response = json.dumps({"status": "ok"})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def complaints_response(request):
    if request.method == 'POST':
        return respond_to_complaint(request)


def respond_to_complaint(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    message = body['message']
    email = body['email']
    message_id = body['message_id']
    first_name = body['first_name']
    message_html = "<p>Dear " + first_name + ",<br><br>" + message + "<br><br>Sincerely,<br>A+Ocean Support Team</p>"
    message = Mail(
        from_email='support@aplusocean.com',
        to_emails=email,
        subject='Support Message Follow-Up',
        html_content=message_html)
    try:
        response = sg.send(message)
    except Exception:
        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')
    if 200 <= int(response.status_code) < 300:
        SupportMessage.objects.filter(message_id=int(message_id)).delete()
        return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')

@csrf_exempt
def get_message(request):
    if request.method == 'GET':
        return get_user_message(request)


def get_user_message(request):
    complaints = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['message_id']
    complaints_results = serializers.serialize('json', SupportMessage.objects.all().order_by('date_sent'))
    for message in complaints_results:
        complaint = UserComplaint(message.message_id, message.first_name, message.last_name, message.email,
                                  message.message, message.date_sent)
    complaints.append(complaint.get_json())
    user_complaint = json.dumps(complaints)
    return HttpResponse(user_complaint, content_type='application/json')
