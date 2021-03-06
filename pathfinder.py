import sys
import json
import time
import multiprocessing
from datetime import datetime
from getpass import getpass
from nasa import Nasa
from rocket import Rocket
from computer import Computer

# version
v = "6"

def default(command=""):
    if command == "":
        print("Command is not specified.")
    else:
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
        sys.exit(1)
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
    tls = input("Do you prefer use HTTPS protocol? (Just enter or other answers except NO will consider as YES) : ")
    if tls == "NO":
        tls = False
    else:
        tls = True
    password = getpass("Type Registration password of targeted Mars (will not be echoed) : ")
    print("Contacting to Mars World...")
    delta = Rocket(host, port, tls)
    res = delta.POST({'Hello': 'Mars World', 'password': password, "v": v}, "planitia/register")
    if res.status_code != 200:
        print("Error caused when connect to Mars")
        print("Status Code: " + str(res.status_code) + ", Server respond : ")
        print(res.text)
        sys.exit(1)
    data = json.loads(res.text)
    if data["code"] != 200:
        print("Error caused when register to Mars")
        print("Error code: " + str(data["code"]) + ", Reason: " + data["comment"])
        sys.exit(1)

    print("Successfully registered to Mars. Configuration file will be saved.")
    config = {
        "host": host,
        "port": port,
        "systemid": data["data"]["systemId"],
        "comment": "registered",
        "tls": tls,
        "intervals": data["data"]["intervals"]
    }
    print("Sending system information to Mars...")

    computer = Computer(data["data"]["publicKey"])

    informationData = computer.generateInformationData()

    encrypted_data = computer.encryptToBase64(json.dumps(informationData))
    nasa.savePublicKey(data["data"]["publicKey"])
    nasa.saveJSON(config)
    Send(delta, "information", encrypted_data, data["data"]["systemId"], False)
    sync()


def sync():
    checkRegistered()
    nasa = Nasa(".")
    config = nasa.getConfiguration()

    computer = Computer(nasa.getPublicKey())
    syncData = computer.generateSyncData(1)
    encrypted_data = computer.encryptToBase64(json.dumps(syncData))
    rocket = Rocket(config["host"], config["port"], config["tls"])
    Send(rocket, "sync", encrypted_data, config["systemid"])


def deregister():
    nasa = Nasa(".")
    nasa.removeConfiguration()
    print("Deregistered successfully.")


def daemon():
    rocket = Rocket(config["host"], config["port"], config["tls"])
    sentDayData = False
    while True:
    #threading.Timer(1, daemon, [computer]).start()
        syncData = computer.generateSyncData(config["intervals"])
        now = datetime.now()
        if sentDayData == True:
            if now.hour != 0 and now.minute != 0:
                sentDayData = False
        else:
            dmesg = computer.generateServiceData("dmesg")
            sentDayData = True
        sentDayData = True
        encrypted_data = computer.encryptToBase64(json.dumps(syncData))
        Send(rocket, "sync", encrypted_data, config["systemid"], True)

        time.sleep(((1000000-now.microsecond)*0.000001)+(config["intervals"]-1))


def Send(rocket, task, data, systemid, isDaemon=True):
    response = rocket.POST({"systemid": systemid, "data": data, "task": task, "v": v}, "planitia/sync")
    try:
        data = json.loads(response.text)
        if data["code"] == 200 and data["comment"] == "success":
            if isDaemon:
                from datetime import datetime
                print("Synced - " + str(datetime.now()))
            else:
                print("Successfully synced to Mars.")
                sys.exit(1)
        elif data["code"] == 305 and data["comment"] == "requireupdate":
            nasa.addConfig("intervals", data["data"])
            informationData = computer.generateInformationData()
            encrypted_data = computer.encryptToBase64(json.dumps(informationData))
            rocket.POST({"systemid": systemid, "data": encrypted_data, "task": "information", "v": v}, "planitia/sync")
            print("Successfully sent system information data to Mars.")
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
            sys.exit(1)
        else:
            return False
    else:
        return True

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()

    if len(sys.argv) < 2:
        default()
    elif sys.argv[1] == "register":
        register()
    elif sys.argv[1] == "deregister":
        deregister()
    elif sys.argv[1] == "sync":
        sync()
    elif sys.argv[1] == "daemon":
        checkRegistered()
        nasa = Nasa(".")
        config = nasa.getConfiguration()
        computer = Computer(nasa.getPublicKey())
        daemon()
    else:
        default(sys.argv[1])
