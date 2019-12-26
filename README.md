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
user@localhost:~/Pathfinder$ sudo apt install python3-cpuinfo python3-psutil python3-bs4 python3-cryptography
```
## Fedora
```bash
[andrew@raspberrypi Mars]$ sudo dnf install python3-beautifulsoup4 python3-psutil python3-cryptography python3-requests
```
## FreeBSD
```bash
root@localhost~:#  pkg install py36-requests py36-psutil py36-beautifulsoup py36-py-cpuinfo py36-distro
```