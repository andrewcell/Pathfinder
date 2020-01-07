import requests
import json
import difflib
import sys
import os
import platform

def checkUpdated(filename):
    print("--------------Validating " + filename + "--------------")
    onlineFile = requests.get("https://raw.githubusercontent.com/andrewcell/Pathfinder/master/" + filename).text
    diff = list(difflib.unified_diff(open("." + "/" + filename, "r").read().strip().splitlines(),
                                      onlineFile.strip().splitlines(), fromfile=filename+".local",
                                      tofile=filename + ".new", lineterm="", n=0))
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
            print("Update completed. " + filename + " available.")
            sys.exit(0)
    print("No option available. Run on proper environment.")
    sys.exit(0)
if __name__ == "__main__":
    print("Checking Newest Update")
    import pathfinder
    print("Current API Version : v" + pathfinder.v)
    del pathfinder
    import nasa
    nasa = nasa.Nasa(".")
    if nasa.fileExists("pathfinder-linux-amd64") or nasa.fileExists("pathfinder-linux-aarch64") or nasa.fileExists("pathfinder-macos") or nasa.fileExists("pathfinder-windowsexe"):
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
    print("Updater Job is completed.")