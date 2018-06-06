import requests
import json

baseurl = 'https://piopiy.telecmi.com/v1/phone2phone';


p2p = {'from': 9894,'appid': 11110,'secret': 'xdcdcdd','to': 9677}

headers = {'content-type': 'application/json'}

r = requests.post(baseurl, data=json.dumps(p2p), headers=headers)


print(r.text)