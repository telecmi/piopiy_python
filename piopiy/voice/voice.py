from .pcmo_call import PCMO
from piopiy.underscore import isNumber,isArray




class Voice:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def call(self, to, piopiy_no, to_or_array_pcmo,options='none'):

        if isinstance(to, int) and isinstance(piopiy_no, int) and isArray(to_or_array_pcmo) or isNumber(to_or_array_pcmo):

            if isArray(to_or_array_pcmo) and any(isinstance(item, dict) for item in to_or_array_pcmo):
              return PCMO(self.appid, self.secret).makePCMO(to, piopiy_no, to_or_array_pcmo, options)
            else:
              return PCMO(self.appid, self.secret).make(to, piopiy_no, to_or_array_pcmo, options)
        else:
            raise NameError('invalid argument type to make call')
