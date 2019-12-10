import pika
import config
import json
import pickle
from django.http import HttpResponse
from classes.EmailData import EmailData
from classes.MessageText import MessageText
from classes.UserComplaint import UserComplaint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import config as config


sg = SendGridAPIClient('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')

def send_notification(email, subject, message_html):
    message = Mail(
        from_email='notifications@aplusocean.com',
        to_emails=email,
        subject=subject,
        html_content=message_html)
    try:
        print("SENDING EMAIL", flush=True)
        response = sg.send(message)
    except Exception as e:
        print("EXCEPTION SENDING EMAIL", flush=True)
        print(e,flush=True)
    return
    #     return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')
    # if 200 <= int(response.status_code) < 300:
    #     return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
    # else:
    #     return HttpResponse(json.dumps({'status': 'error'}), content_type='application/json')

print("NOTIFICATIONS TASK STARTING", flush=True)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
channel = connection.channel()
print(' [*] Waiting for notifications', flush=True)
channel.exchange_declare(exchange='notifications', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='notifications', queue=queue_name, routing_key="notifications")

def callback(ch, method, properties, body):
    body = pickle.loads(body)
    print(" [x] Received %r" % body, flush=True)
    print(body["email"], flush=True)
    message = MessageText(body["type"], body)
    message_text = message.get_message_text()
    print(message_text, flush=True)
    subject = message.get_message_subject()
    print(subject, flush=True)
    send_notification(body["email"], subject, message_text)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

sg = SendGridAPIClient('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')
