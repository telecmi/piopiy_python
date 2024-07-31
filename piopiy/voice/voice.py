import requests
import json

host = "https://piopiy.telecmi.com/v1/make_call"


class Voice:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def make(self, to, piopiy_no, answer_url):

        if isinstance(to, int) and isinstance(piopiy_no, int) and isinstance(answer_url, str):
            data = {'from': piopiy_no, 'appid': self.appid,
                    'secret': self.secret, 'to': to, 'answer_url': answer_url}
            headers = {'content-type': 'application/json'}
            return requests.post(host, data=json.dumps(data), headers=headers).text
        else:

            raise NameError('invalid argument type to make call')
