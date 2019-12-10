class EmailData:

    def __init__(self, first_name, email, subject, message):
        self.first_name = first_name
        self.email = email
        self.subject = subject
        self.message = message

    def get_message_data(self):
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "skoop@uchicago.edu",
                        "Name": "A+Ocean"
                    },
                    "To": [
                        {
                            "Email": self.email,
                            "Name": self.first_name
                        }
                    ],
                    "Subject": self.subject,
                    "TextPart": self.subject,
                    "HTMLPart": self.message,
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        return data

