import requests
import json

host = "https://piopiy.telecmi.com/v1/call/action"


class Hangup:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def hangup(self, uuid):

        if isinstance(uuid, str):
            data = {'appid': self.appid,
                    'secret': self.secret, 'cmiuuid': uuid, 'action': 'hangup'}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to make call')
