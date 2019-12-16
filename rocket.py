import requests
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')
csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

class Rocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self protocol = "http://"
    def returnHost(self):
        return self.host
    def returnPort(self):
        return self.port
    def HIT(self, path):
        return requests.get(self.protocol + self.host + ":" + self.port + "/" + path)
    def POST(self, data, path):
        page = self.HIT("/admin/login")
        soup = BeautifulSoup(page, 'lxml')
        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

        return requests.post("http://"+self.host+":"+self.port+"/"+path, data=data)

   
