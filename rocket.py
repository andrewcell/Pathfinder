import requests
from bs4 import BeautifulSoup
class Rocket:
    def __init__(self, host, port, TLS):
        self.host = host
        self.port = port
        if not TLS:
            self.protocol = "http://"
            print("TLS is disabled. Data is still encrypted, but it is good to use TLS. ")
        else:
            self.protocol = "https://"
        self.request = requests.Session()

    def returnHost(self):
        return self.host

    def returnPort(self):
        return self.port

    def HIT(self, path):
        return self.request.get(self.protocol + self.host + ":" + self.port + "/" + path)

    def getCSRF(self):
        page = self.HIT("admin/login")
        soup = BeautifulSoup(page.text, "html.parser")
        token = soup.find('input', {'name': '_csrf'})['value']
        return token

    def POST(self, data, path):
        token = self.getCSRF()
        data["_csrf"] = token
        return self.request.post(self.protocol+self.host+":"+self.port+"/"+path, data=data)

   
