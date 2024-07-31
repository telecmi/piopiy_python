import requests
import json

host = "https://piopiy.telecmi.com/v1/call/action"


class Hold:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def hold(self, uuid):

        if isinstance(uuid, str):
            data = {'appid': self.appid,
                    'secret': self.secret, 'cmiuuid': uuid, 'action': 'hold'}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to hold call')

    def unhold(self, uuid):

        if isinstance(uuid, str):
            data = {'appid': self.appid,
                    'secret': self.secret, 'cmiuuid': uuid, 'action': 'unhold'}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to unhold call')

    def toggle(self, uuid):

        if isinstance(uuid, str):
            data = {'appid': self.appid,
                    'secret': self.secret, 'cmiuuid': uuid, 'action': 'holdToggle'}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to toggle call')
