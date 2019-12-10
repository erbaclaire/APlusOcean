import requests
import json
import base64
from django.conf import settings as djangoSettings


class DataLoader:

    def __init__(self, service, endpoint):
        self.service = service
        self.endpoint = endpoint

    def get_data(self):
        try:
            response = requests.get(self.service + self.endpoint)
            response_data = json.loads(response.text)
        except:
            response_data = []
        finally:
            return response_data

    def get_data_with_images(self):
        try:
            response = requests.get(self.service + self.endpoint)
            response_data = json.loads(response.text)
            for item in response_data:
                if item['fields']['item_pic'] != '':
                    pic = item['fields']['item_pic']
                    encoded = pic.encode('ascii')
                    imgdata = base64.decodebytes(encoded)
                    filename = str(item['pk']) + '.jpg'
                    with open(djangoSettings.STATIC_ROOT + "/" + filename, 'wb') as f:
                        f.write(imgdata)
                        f.close()
                    item['fields']['item_pic'] = filename
                else:
                    item['fields']['item_pic'] = 'download.png'
        except:
            response_data = []
        finally:
            return response_data

    def get_with_data(self, data):
        try:
            response = requests.get(self.service + self.endpoint, data=data)
            response_data = json.loads(response.text)
        except:
            response_data = []
        finally:
            return response_data

    def get_with_data_and_images(self, data):
        try:
            response = requests.get(self.service + self.endpoint, data=data)
            response_data = json.loads(response.text)
            for item in response_data:
                if item['fields']['item_pic'] != '':
                    pic = item['fields']['item_pic']
                    encoded = pic.encode('ascii')
                    imgdata = base64.decodebytes(encoded)
                    filename = str(item['pk']) + '.jpg'
                    with open(djangoSettings.STATIC_ROOT + "/" + filename, 'wb') as f:
                        f.write(imgdata)
                        f.close()
                    item['fields']['item_pic'] = filename
                else:
                    item['fields']['item_pic'] = 'download.png'
        except:
            response_data = []
        finally:
            return response_data

    def post_data(self, data):
        try:
            response = requests.post(self.service + self.endpoint, data=data)
            response_data = response.json()
        except:
            response_data = []
        finally:
            return response_data
