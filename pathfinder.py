import sys
import json
import time
from getpass import getpass
from nasa import Nasa
from rocket import Rocket
from computer import Computer


# def register():

def default(command=""):
    print(str(command) + " - Wrong command")
    print("""
    You must align specific command from below commands
    ---
    register - Register to Mars World.
    deregister - Remove configuration data received from Mars World.
    sync - Manually sync right now
    daemon - Run as infinite loop(Daemon)
    """)
    registered = checkRegistered(False)
    if not registered:
        print("Notice: It seems you must register to Mars first.")


def register():
    nasa = Nasa(".")
    if nasa.fileExists("pathfinder.key") == True or nasa.fileExists("pathfinder.json") == True:
        print("This system is already registered. For re-register, de-register first.")
        exit(1)
    print("Welcome to register program of Pathfinder towards to Mars.")
    while True:
        host = input("Type Mars World or compatible host (Not URL-scheme) : ")
        if host == "":
            print("You entered blank hostname.")
        else:
            break
    port = input("Type Mars World port number(Just enter or out-range will be 443 : ")
    if port == "" or int(port) <= 1 or int(port) >= 65535:
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
    data = json.loads(res.text)
    if data["code"] != 200:
        print("Error caused when register to Mars")
        print("Error code: " + str(data["code"]) + ", Reason: " + data["comment"])
        exit(1)

    print("Successfully registered to Mars. Configuration file will be saved.")
    config = {
        "host": host,
        "port": port,
        "systemid": data["data"]["systemId"],
        "comment": "registered"
    }
    print("Sending system information to Mars...")

    computer = Computer(data["data"]["publicKey"])

    informationData = computer.generateInformationData()

    encrypted_data = computer.encryptToBase64(json.dumps(informationData))
    nasa.savePublicKey(data["data"]["publicKey"])
    nasa.saveJSON(config)
    Send("information", encrypted_data, config)



def sync():
    checkRegistered()
    nasa = Nasa(".")
    config = nasa.getConfiguration()

    computer = Computer(nasa.getPublicKey())
    syncData = computer.generateSyncData()
    encrypted_data = computer.encryptToBase64(json.dumps(syncData))
    Send("sync", encrypted_data, config)


def deregister():
    nasa = Nasa(".")
    nasa.removeConfiguration()
    print("Deregistered successfully.")


def Send(task, data, config):
    rocket = Rocket(config["host"], config["port"])
    response = rocket.POST({"systemid": config["systemid"], "data": data, "task": task}, "planitia/sync")
    try:
        data = json.loads(response.text)
        if data["code"] == 200 and data["comment"] == "success":
            print("Successfully synced to Mars.")
            exit(1)
        else:
            print("Error caused. Here is respond : " + response.text)
    except json.decoder.JSONDecodeError:
        print("JSON Parse Error caused. Status code : " + str(response.status_code))


def checkRegistered(terminate=True):
    nasa = Nasa(".")
    data = nasa.returnJSON()
    if data["comment"] == "notfound":
        if terminate:
            print("This system is not registered. Pathfinder require register to work.")
            exit(1)
        else:
            return False
    else:
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        default()
    elif sys.argv[1] == "register":
        register()
    elif sys.argv[1] == "deregister":
        deregister()
    elif sys.argv[1] == "sync":
        sync()

    else:
        default(sys.argv[1])
        # cpu_temp = putil.sensors_temperatures().item
