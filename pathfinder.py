import requests
import psutil
import sys
import json
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
    print("Welcome to register program of Pathfinder towards to Mars.")
    host = input("Type Mars World or compatible host (Not URL-scheme) : ")
    port = input("Type Mars World port number(Just enter or out-range will be 443 : ")
    if port == "" or int(port) <= 1 or int(port) >=65535:
        port = 443
    print("Contacting to Mars World...")
    delta = Rocket(host, port)
    
    res = delta.POST({'Hello': 'World'}, "planitia/register")
    if res.status_code != "200":
        print("Error to register to Mars")
        print("Status Code: " + str(res.status_code) + ", Server respond : ")
        print(res.text)
        exit(1)
        # {code: 200, comment: success, data: {publicKey: "-----BEGIN ...", systemId: "asdjfnasdfnkasjdf"},}
    data = json.loads(res.text)
    if data["code"] != 200:
        print("Error to register to Mars")
        print("Error code: " + str(data["code"]) + ", Reason: " + data["comment"])



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
