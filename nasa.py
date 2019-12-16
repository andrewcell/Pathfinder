import json

class Nasa:
    def __init__(self, path):
        self.path = path
    def load(self):
        try:
            self.jsonfile = open(self.path + "/pathfinder.json", "r")
            self.pubkey = open(self.path + "/pathfinder.key", "r")
        except FileNotFoundError:
            self.jsonfile = "{\"comment\": \"notfound\"}"
            self.pubkey = "notfound"    
    def returnPath(self):
        return str(self.path)
    def returnKey(self):
        return str(self.pubkey)
    def returnJSONRaw(self):
        return str(self.jsonfile)
    def returnJSON(self):
        self.load()
        return json.loads(self.jsonfile)


