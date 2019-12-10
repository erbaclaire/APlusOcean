import json


class UserComplaint:

    def __init__(self, id, first_name, last_name, email, message, date):
        self.id = str(id),
        self.first_name = str(first_name),
        self.last_name = str(last_name),
        self.email = str(email),
        self.message = str(message),
        self.date = str(date)

    def get_json(self):
        data = {"message_id": self.id[0],
                "first_name": self.first_name[0],
                "last_name": self.last_name[0],
                "email": self.email[0],
                "message": self.message[0],
                "date": self.date}
        return data

