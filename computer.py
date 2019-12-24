import base64
import platform
import psutil
import socket
import distro

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import hashes
from cpuinfo import get_cpu_info
from datetime import datetime
import time
from nasa import Nasa

class Computer:
    def __init__(self, publickey):
        self.key = load_pem_public_key(data=publickey.encode(), backend=default_backend())

    def encryptToBase64(self, string, encoding="ascii"):
        byte = string.encode()
        cipher = self.key.encrypt(byte, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return base64.b64encode(cipher)

    def generateInformationData(self):
        data = {
            "name": self.getHostname(),
            "architecture": self.getArchitecture(),
            "cpu_name": get_cpu_info()["brand"],
            "kernel_name": self.getKernelName(),
            "kernel_version": self.getKernelVersion(),
            "ram_size": psutil.virtual_memory()[0],
            "distribution": self.getDistribution(),
            "datetime": self.getTimedata()
        }
        return data

    def generateSyncData(self):
        data = {
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory()[2],
            "network_usage": self.getNetworkUsage(),
            "localip": self.getLocalIPAddress(),
            "datetime": self.getTimedata()
        }
        return data

    def getTimedata(self):
        now = datetime.now()
        data = {
            "queryTime": str(now),
            "queryTimeUnix": time.time(),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "microsecond": now.microsecond
        }
        return data

    def getHostname(self):
        return platform.node()


    def getArchitecture(self):
        default = {
            'amd64': 'amd64',
            'AMD64': 'amd64',
            'x86_64': 'amd64',
            'i386': 'i386',
            'i486': 'i386',
            'i586': 'i386',
            'i686': 'i386',
            'armv7l': 'arm',
            'armv7': 'arm',
            'armv8': 'aarch64',
            'armv8l': 'aarch64'

        }
        arch = default.get(platform.machine(), lambda: "unknown")
        return arch

    def getKernelName(self):
        return platform.system()

    def getKernelVersion(self):
        return platform.release()

    def getNetworkUsage(self):
        #if platform.system() == "Linux":

        psutil_value = psutil.net_io_counters()
        sent = psutil_value.bytes_sent
        recv = psutil_value.bytes_recv
        return {"sent": sent, "recv": recv}

    def getLocalIPAddress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]

    def getDistribution(self):
        system = platform.system()
        data = {
            "name": "",
            "version": ""
        }
        if system == "Windows":
            data["name"] = "Windows"
        elif system == "Linux":
            dist = distro.linux_distribution(full_distribution_name=True)
            data["name"] = dist[0]
            data["version"] = dist[1]
        elif system == "FreeBSD":
            data["name"] = system
            data["version"] = platform.release()
        elif system == "Darwin":
            data["name"] = "macOS"
            data["version"] = platform.mac_ver()[0]
        else:
            data["name"] = "Unknown"
            data["version"] = "0"
        return data


