from underscore import isString
from bridge import connect
from input import input
import json


class Action:
    def __init__(self):
        self.action = []

    def playMusicName(self, file_name):

        if isString(file_name):
            self.action.append({
                "action": "play",
                "file_name": file_name
            })
        else:
            raise NameError('filename is required to play')

    def playMusicURL(self, file_url):

        if isString(file_url):
            self.action.append({
                "action": "play",
                "file_url": file_url
            })
        else:
            raise NameError('fileurl is required to play')

    def record(self):
        self.action.append({"action": "record"})

    def hangup(self):
        self.action.append({"action": "hangup"})

    def forward(self, to, piopiy_no, option='none'):
        bridge = connect(to, piopiy_no, option)
        self.action.append(bridge)

    def input(self, action_url, option='none'):
        dtmf = input(action_url, option)
        self.action.append(dtmf)

    def PCMO(self):
        return json.dumps(self.action)
