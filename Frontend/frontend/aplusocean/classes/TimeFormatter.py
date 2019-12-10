import datetime

class TimeFormatter:

    def __init__(self, data):
        self.data = data

    def get_formatted_time(self):
        for item in self.data:
            if item['fields']['auction_start_time'] is not None:
                item['fields']['auction_start_time'] = datetime.datetime.strptime((datetime.datetime.strptime(
                    (item['fields']['auction_start_time']).replace('Z', ''), '%Y-%m-%dT%H:%M:%S')).strftime(
                    '%m/%d/%Y %I:%M %p'), '%m/%d/%Y %I:%M %p')
            if item['fields']['auction_end_time'] is not None:
                item['fields']['auction_end_time'] = datetime.datetime.strptime((datetime.datetime.strptime(
                    (item['fields']['auction_end_time']).replace('Z', ''), '%Y-%m-%dT%H:%M:%S')).strftime(
                    '%m/%d/%Y %I:%M %p'), '%m/%d/%Y %I:%M %p')
        return self.data
