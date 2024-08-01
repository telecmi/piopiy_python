from .pcmo_call import PCMO
from piopiy.underscore import isNumber, isString,isArray




class Voice:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def call(self, to, piopiy_no, to_or_array,options='none'):

        if isinstance(to, int) and isinstance(piopiy_no, int) and isArray(to_or_array) or isNumber(to_or_array):
            return PCMO(self.appid, self.secret).make(to, piopiy_no, to_or_array, options)
        else:
            raise NameError('invalid argument type to make call')
