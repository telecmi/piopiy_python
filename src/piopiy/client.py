from voice import Voice


class RestClient:

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def make(self, to, piopiy_no, answer_url):
        return Voice(self.appid, self.secret).make(to, piopiy_no, answer_url)
