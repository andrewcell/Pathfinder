import json
import os
import sys

class Nasa:
    def __init__(self, path):
        self.path = path
        if getattr(sys, 'frozen', False):
            self.__location__ = os.path.dirname(sys.executable)
        else:
            self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.load()

    def load(self):
        try:
            self.jsonfile = open(self.__location__ + "/pathfinder.json", "r").read()
            self.pubkey = open(self.__location__ + "/pathfinder.key", "r").read()
        except FileNotFoundError:
            self.jsonfile = "{\"comment\": \"notfound\"}"
            self.pubkey = "notfound"

    def savePublicKey(self, pem):
        key = open(os.path.join(self.__location__, "pathfinder.key"), "w")
        key.write(str(pem))
        key.close()

    def saveJSON(self, dict):
        jsonfile = json.dumps(dict)
        key = open(os.path.join(self.__location__, "pathfinder.json"), "w")
        key.write(jsonfile)
        key.close()

    def getPublicKey(self):
        return self.pubkey

    def getConfiguration(self):
        return json.loads(open(self.path + "/pathfinder.json", "r").read())

    def removeConfiguration(self):
        json = self.path + "/pathfinder.json"
        key = self.path + "/pathfinder.key"
        if os.path.isfile(json):
            os.remove(json)
        if os.path.isfile(key):
            os.remove(key)

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

    def addConfig(self, optionName, optionValue):
        dict = self.getConfiguration()
        dict[optionName] = optionValue
        self.saveJSON(dict)

    def returnServiceConfiguration(self, serviceName):
        try:
            config = json.loads(open(self.__location__ + "/services/" + serviceName + ".json", "r").read())
        except Exception as E:
            return {"comment": "notfound"}
        else:
            return {serviceName: config}

    def createServiceDirectory(self):
        try:
            os.mkdir(self.__location__ + "/services")
        except OSError:
            print("Failed to create Service options directory.")

