# Pathfinder
Server status reporting program for Unix-like OS.
Require [Mars World](https://github.com/andrewcell/Mars) as central server

# Install Python dependencies
 - psutil needs GCC for install via pip. If install on server, it is recommended to use package manager to install dependencies.
## virtualenv
```bash
bash> pip install -r requirements.txt
```
## OpenSUSE
```bash
user@localhost:~> sudo zypper install python3-requests python3-psutil python3-beautifulsoup4 python3-py-cpuinfo
```
## Ubuntu
```bash
user@localhost:~/Pathfinder$ sudo apt install python3-cpuinfo python3-psutil python3-bs4 python3-cryptography python3-distro
```
## Fedora
```bash
[andrew@raspberrypi Mars]$ sudo dnf install python3-beautifulsoup4 python3-psutil python3-cryptography python3-requests python3-distro
```
## FreeBSD
```bash
root@localhost~:#  pkg install py36-requests py36-psutil py36-beautifulsoup py36-py-cpuinfo py36-distro
```

# Prebuilt
 - You can find binary in releases. Every commit, prebuilt file for Windows, Linux, macOS will appear. It is automated using Travis CI, pyinstaller.

# Update
If you installed or want update via Git, you need to install gitpython.
```bash
bash-3.2 ~# pip3 install gitpython
```
Run updater.py. This will get update from Github.
 
# Updater
Recently, updater is added to Pathfinder.
just run updater.py. updater will replace script files from Github.

## Install
Updater can operate as installer. just place updater to directory that you want to install pathfinder. Updater will automatically download require files include python scripts. If you want get pyinstaller prebuilt file, make empty file named "DOWNLOAD_HERE" (without quotes). 

# Build Status
[![Build Status](https://travis-ci.org/andrewcell/Pathfinder.svg?branch=master)](https://travis-ci.org/andrewcell/Pathfinder)