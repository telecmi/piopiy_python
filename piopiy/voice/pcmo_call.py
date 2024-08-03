import requests
from piopiy.underscore import isIND,isNumber,isArray,isObject
from piopiy.action import Action;
import json


ind_voice = { "host": "https://rest.telecmi.com", "path": "/v2/ind_pcmo_make_call" };

glob_voice = { "host": "https://rest.telecmi.com", "path": "/v2/global_pcmo_make_call" };




class PCMO:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret


    def make(self, to, piopiy_no, forward_number, option='none'):

        if isNumber(to) and isNumber(piopiy_no) and isNumber(forward_number) or isArray(forward_number):
            duration = 5400
            extra_params = {}

            pcmo = Action()
            pcmo.call(forward_number, piopiy_no, option)
            print(pcmo.PCMO())
            if isObject(option):
                duration = option.get('duration', 5400)
                extra_params = option.get('extra_params', {})
                
            options_data = {"appid": self.appid,
            "secret": self.secret,
            "extra_params": extra_params,
            "from": piopiy_no,
            "duration": duration,
            "pcmo": pcmo.PCMO(),
            "to": to}

            host = ind_voice if isIND(piopiy_no) else glob_voice

            headers = {'content-type': 'application/json'}
           
            return requests.post(host['host']+host['path'], data=json.dumps(options_data), headers=headers).json()
        

    def makePCMO(self, to, piopiy_no, pcmo, option='none'):

        if isNumber(to) and isNumber(piopiy_no) and  isArray(pcmo):
            duration = 5400
            extra_params = {}

          
            if isObject(option):
                duration = option.get('duration', 5400)
                extra_params = option.get('extra_params', {})
                
            options_data = {"appid": self.appid,
            "secret": self.secret,
            "extra_params": extra_params,
            "from": piopiy_no,
            "duration": duration,
            "pcmo": pcmo,
            "to": to}

            host = ind_voice if isIND(piopiy_no) else glob_voice

            headers = {'content-type': 'application/json'}
           
            return requests.post(host['host']+host['path'], data=json.dumps(options_data), headers=headers).json()
