from twilio.rest import Client

class twilio:
    def __init__(self):
        self.account_sid = 'ACe53c89870e6888ae8288898354fde'
        self.auth_token = 'eeae36ef14bf7d55fdf10ae5b3d@cfe8'
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, body, from_, to):
        message = self.client.messages.create(
            body=body,
            from_=from_,
            to=to
        )
        return message
