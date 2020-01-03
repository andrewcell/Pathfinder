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
        self.disk = self.getDiskIOUsage()
        self.network = self.getNetworkUsage()

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

    def generateSyncData(self, intervals):
        disk = self.getDiskIOUsage()
        network = self.getNetworkUsage()

        data = {
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory()[2],
            "network_usage": self.getNetworkUsage(),
            "localip": self.getLocalIPAddress(),
            "disk_read": self.getIOSpeed(disk["read"], self.disk["read"], intervals),
            "disk_write": self.getIOSpeed(disk["write"], self.disk["write"], intervals),
            "network_speed_send": self.getIOSpeed(network["sent"], self.network["sent"], intervals),
            "network_speed_receive": self.getIOSpeed(network["recv"], self.network["recv"], intervals),
            "datetime": self.getTimedata()
        }
        self.disk = disk
        self.network = network

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
            'x86': 'i386',
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
            try:
                #__import__('wmi').find_module('WMI')
                from wmi import WMI
                for os in WMI().Win32_OperatingSystem():
                    data["name"] = os.Caption.replace("Microsoft ", "")
                    data["version"] = os.Version
            except ImportError:
                data["name"] = "Windows"
                data["version"] = platform.version()
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

    def getDiskIOUsage(self):
        io = psutil.disk_io_counters()
        read = io.read_bytes
        write = io.write_bytes
        return {"read": read, "write": write}

    def getIOSpeed(self, A, B, interval):
        return (int(A) - int(B)) / interval
