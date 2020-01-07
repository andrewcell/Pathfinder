import requests
import json
import difflib
import sys


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

if __name__ == "__main__":
    print("Checking Newest Update")
    import pathfinder
    print("Current API Version : v" + pathfinder.v)
    del pathfinder
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