import requests
import json

host = "https://piopiy.telecmi.com/v1/call/action"


class Transfer:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def transfer(self, uuid, transfer_url):

        if isinstance(uuid, str) and isinstance(transfer_url, str):
            data = {'appid': self.appid,
                    'secret': self.secret, 'cmiuuid': uuid, 'action': 'transfer', 'transfer_url': transfer_url}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to transfer call')
