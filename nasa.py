import json
import os


class Nasa:
    def __init__(self, path):
        self.path = path
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def load(self):
        try:
            self.jsonfile = open(self.path + "/pathfinder.json", "r")
            self.pubkey = open(self.path + "/pathfinder.key", "r")
        except FileNotFoundError:
            self.jsonfile = "{\"comment\": \"notfound\"}"
            self.pubkey = "notfound"

    def savePublicKey(self, pem):
        key = open(os.path.join(self.__location__, "pathfinder.key"), "w")
        key.write(str(pem))
        print(self.__location__)
        key.close()

    def saveJSON(self, dict):
        jsonfile = json.dumps(dict)
        key = open(os.path.join(self.__location__, "pathfinder.json"), "w")
        key.write(jsonfile)
        key.close()

    def fileExists(self, filename):
        return os.path.exists(os.path.join(self.__location__, filename))

    def returnPath(self):
        return str(self.path)

    def returnKey(self):
        return str(self.pubkey)

    def returnJSONRaw(self):
        return str(self.jsonfile)

    def returnJSON(self):
        self.load()
        return json.loads(self.jsonfile)
