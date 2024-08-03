from .voice import Voice
from .hold import Hold
from .hangup import Hangup


class RestClient:

    def __init__(self, appid, secret):

        if isinstance(appid, int) and isinstance(secret, str):
          
         self.appid = appid
         self.secret = secret
         self.voice = Voice(self.appid, self.secret)
        else:
              raise NameError('appid and secret type is invalid')

    def hold(self, uuid):
        return Hold(self.appid, self.secret).hold(uuid)

    def unhold(self, uuid):
        return Hold(self.appid, self.secret).unhold(uuid)

    def toggle(self, uuid):
        return Hold(self.appid, self.secret).toggle(uuid)

    def hangup(self, uuid):
        return Hangup(self.appid, self.secret).hangup(uuid)
