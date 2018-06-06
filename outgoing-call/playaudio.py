import requests
import json

baseurl = 'https://piopiy.telecmi.com/v1/playaudio';


playaudio = {
    'appid': 11110,
    'secret': 'xdcdcdd',
    'to': 9677,
    'play': {

        "url": "http://example.com/music/thanks.wav"

    }
}

headers = {'content-type': 'application/json'}

r = requests.post(baseurl, data=json.dumps(playaudio), headers=headers)


print(r.text)