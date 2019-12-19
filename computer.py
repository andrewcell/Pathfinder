import base64
import platform
import psutil
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import hashes
from cpuinfo import get_cpu_info
from nasa import Nasa

class Computer:
    def __init__(self, publickey):
        self.key = load_pem_public_key(data=bytearray(publickey, "ascii"), backend=default_backend())

    def encryptToBase64(self, string, encoding="ascii"):
        byte = string.encode()
        cipher = self.key.encrypt(byte, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(),
                                                     label=None))
        return base64.b64encode(cipher)

    def generateInformationData(self):
        data = {
            "name": self.getHostname(),
            "architecture": self.getArchitecture(),
            "cpu_name": get_cpu_info()["brand"],
            "kernel_name": self.getKernelName(),
            "kernel_version": self.getKernelVersion(),
            "ram_size": psutil.virtual_memory()[0],
        }
        return data

    def generateSyncData(self):
        data = {
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory()[2],

        }
        return data

    def getHostname(self):
        return platform.node()

    def getArchitecture(self):
        return platform.machine()

    def getKernelName(self):
        return platform.system()

    def getKernelVersion(self):
        return platform.release()
