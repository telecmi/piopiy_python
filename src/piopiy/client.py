from voice import Voice
from hold import Hold
from hangup import Hangup
from transfer import Transfer


class RestClient:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def make(self, to, piopiy_no, answer_url):
        return Voice(self.appid, self.secret).make(to, piopiy_no, answer_url)

    def hold(self, uuid):
        return Hold(self.appid, self.secret).hold(uuid)

    def unhold(self, uuid):
        return Hold(self.appid, self.secret).unhold(uuid)

    def toggle(self, uuid):
        return Hold(self.appid, self.secret).toggle(uuid)

    def hangup(self, uuid):
        return Hangup(self.appid, self.secret).hangup(uuid)
