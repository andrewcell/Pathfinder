import requests
import json
import difflib
import sys
import os
import platform

def checkUpdated(filename):
    print("--------------Validating " + filename + "--------------")
    try:
        onlineFile = requests.get("https://raw.githubusercontent.com/andrewcell/Pathfinder/master/" + filename).text
        diff = list(difflib.unified_diff(open("." + "/" + filename, "r").read().strip().splitlines(),
                                          onlineFile.strip().splitlines(), fromfile=filename+".local",
                                          tofile=filename + ".new", lineterm="", n=0))
    except FileNotFoundError:
        return True, onlineFile
    if not diff:
        print("No update found for " + filename + ".")
        return False, ""
    else:
        print("Recent changes of " + filename + " : ")
        for line in diff:
            print(line)
        return True, onlineFile

def updateFile(filename, newFile):
    file = open("./" + filename, "w")
    file.write(newFile)
    file.close()
    print(filename + " is updated.")

def pyinstallerUpdate():
    path = os.path.dirname(sys.executable)
    print("Pyinstaller prebuilt detected. Updating prebuilt file.")
    print("Retrieving Latest release from Github...")
    latest = json.loads(requests.get("https://api.github.com/repos/andrewcell/Pathfinder/releases").text)[0]
    print("Downloading " + latest["tag_name"] + "...")
    machine = platform.machine()
    system = platform.system()
    if machine.endswith("86"): # Check is 32bit only system.
        print("Prebuilt for 32bit system is not available.")
        sys.exit(1)

    if system == "Darwin": # macOS only have amd64 system.
        filename = "pathfinder-macos"
    elif machine.startswith("arm", 0, 3) or machine == "aarch64": # Detect ARM
        if system != "Linux": # If is not Linux
            print("Prebuilt for ARM 64bit system only available in Linux.")
            sys.exit(1)
        else:
            filename = "pathfinder-linux-aarch64"
    elif system == "Linux":
        filename = "pathfinder-linux-amd64"
    elif system == "Windows":
        if machine != "x86_64":
            print("Prebuilt for amd64 is only available item on Windows.") # Maybe run on Windows on Arm
        else:
            filename = "pathfinder-windows.exe"

    print("Downloading - " + filename)
    for asset in latest["assets"]:
        if asset["name"] == filename:
            import shutil
            data = requests.get(asset["browser_download_url"], stream=True)
            with open(path + "/" + filename, "wb") as f:
                data.raw.decode_content = True
                shutil.copyfileobj(data.raw, f)
            print("Download Completed - " + filename)
            if not sys.platform.startswith('win'):
                os.chmod(path + "/" + filename, 0o775)
            print("Update completed. " + filename + " available.")
            try:
                os.remove(path + "/" + "DOWNLOAD_HERE")
            except FileNotFoundError:
                pass
            sys.exit(0)
    print("No option available. Run on proper environment.")
    sys.exit(0)
if __name__ == "__main__":
    print("Checking Newest Update")
    try:
        import pathfinder
        print("Current API Version : v" + pathfinder.v)
        del pathfinder
    except ImportError:
        print("Looks like pathfinder is not installed here or corrupted. Proceed update will install pathfinder to updater locaton.")
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    if os.path.exists(os.path.join(path, "pathfinder-linux-amd64")) or os.path.exists(os.path.join(path, "pathfinder-linux-aarch64")) or os.path.exists(os.path.join(path, "DOWNLOAD_HERE")) or os.path.exists(os.path.join(path, "pathfinder-macos")) or os.path.exists(os.path.join(path, "pathfinder-windows.exe")):
        pyinstallerUpdate()
    try:
        print("Trying Git Pull from origin...")
        import git
        g = git.cmd.git(".")
        g.pull()
    except ImportError:
        print("GitPython not found. Trying manual update procedure.")
    except Exception as e:
        print("Git error caused. Error Message : " + e)

    acceptance = input("Do you accept updater.py to modify script files? Any changes not on online will discard. Type 'Agree' : ")
    if not acceptance == "Agree":
        print("Accept is required to update.")
        sys.exit(1)
    result = json.loads(requests.get("https://api.github.com/repos/andrewcell/Pathfinder/releases").text)
    FILENAME = ["nasa.py", "pathfinder.py", "computer.py", "rocket.py", "README.md", "requirements.txt", "updater.py"]
    for file in FILENAME:
        requireUpdate, newFile = checkUpdated(file)
        if requireUpdate:
            updateFile(file, newFile)
            print("--------------" + file + " Updated--------------")
    print("Updater Job is completed.")