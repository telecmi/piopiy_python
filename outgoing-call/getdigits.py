import requests
import json

baseurl = 'https://piopiy.telecmi.com/v1/getdigits';


getdigits = {
    'appid': 11110,
    'secret': 'xdcdcdd',
    'to': 9677, 
    'get': {
        'start': "http://example.com/waiting.wav",
        'invalid': "http://example.com/invalid.wav",
        'min': 1,
        'max': 1,
        'post': "http://example.com/option"
    }
}

headers = {'content-type': 'application/json'}

r = requests.post(baseurl, data=json.dumps(getdigits), headers=headers)


print(r.text)