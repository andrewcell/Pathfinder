import requests
import psutil
import sys
import json
from getpass import getpass
#import argparse
from nasa import Nasa
from rocket import Rocket
#def register():

def default(command=""):
    print(str(command) + " - Wrong command")
    print("""
    You must align specific command from below commands
    ---
    register - Register to Mars World.
    unregister - Remove from Mars World.
    sync - Manually sync right now
    daemon - Run as infinite loop(Daemon)
    """)
    registered = checkRegistered()
    if registered == False:
        print("Notice: It seems you must register to Mars first.")

def register():
    nasa = Nasa(".")
    if nasa.fileExists("pathfinder.key") == True or nasa.fileExists("pathfinder.json") == True:
        print("This system is already registered. For re-register, un-register first.")
        exit(1)
    print("Welcome to register program of Pathfinder towards to Mars.")
    while True:
        host = input("Type Mars World or compatible host (Not URL-scheme) : ")
        if host == "":
            print("You entered blank hostname.")
        else:
            break
    port = input("Type Mars World port number(Just enter or out-range will be 443 : ")
    if port == "" or int(port) <= 1 or int(port) >=65535:
        port = 443
    password = getpass("Type Registration password of targeted Mars (will not be echoed) : ")
    print("Contacting to Mars World...")
    delta = Rocket(host, port) 
    res = delta.POST({'Hello': 'Mars World', 'password': password, "v": 0}, "planitia/register")
    if res.status_code != 200:
        print("Error caused when connect to Mars")
        print("Status Code: " + str(res.status_code) + ", Server respond : ")
        print(res.text)
        exit(1)
        # {code: 200, comment: success, data: {publicKey: "-----BEGIN ...", systemId: "asdjfnasdfnkasjdf"},}
    data = json.loads(res.text)
    if data["code"] != 200:
        print("Error caused when register to Mars")
        print("Error code: " + str(data["code"]) + ", Reason: " + data["comment"])
        exit(1)
    print(data)
    nasa.savePublicKey(data["data"]["publicKey"])
    print("Successfully registered to Mars. Configuration file will be saved.")
    config = {
        "host": host,
        "port": port,
        "systemid": data["data"]["systemId"]
    }
    nasa.saveJSON(config)


def checkRegistered():
#    print("Checking is registered..")
    nasa = Nasa(".")
    data = nasa.returnJSON()
    if data["comment"] == "notfound":
        return False
    else:
        return True
#    print(str(nasa.returnJSON()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        default()
    #parser = argparse.ArgumentParser(description='Commands?')
    #pr
    elif sys.argv[1]=="register":
        register()        
    elif sys.argv[1]=="unregister":
        print("unregister")
    elif sys.argv[1]=="sync":
        print("asd")
    else:
       default(sys.argv[1]) 
   #cpu_temp = putil.sensors_temperatures().item
