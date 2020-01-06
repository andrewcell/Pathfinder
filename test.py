import base64

from nasa import Nasa
from computer import Computer
from rocket import Rocket
import sys
import time
import traceback
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
if __name__=="__main__":
    try:
        print("Testing Nasa")
        nasa = Nasa(".")
        nasa.removeConfiguration()
        nasa.saveJSON({"host": "127.0.0.1",
                       "port": "8080",
                       "systemid": "systemidtarget",
                       "comment": "registered",
                       "tls": False})
        nasa.savePublicKey("-----BEGIN RSA PUBLIC KEY-----")
        nasa.load()
        nasa.addConfig("interval", 3)
        jsonExists = nasa.fileExists("pathfinder.json")
        keyExists = nasa.fileExists("pathfinder.key")
        if not jsonExists or not keyExists:
            print("Save configuration failed.")
        if nasa.returnJSONRaw() != '{"host": "127.0.0.1", "port": "8080", "systemid": "systemidtarget", "comment": "registered", "tls": false}':
            print("Raw Configuration mismatch")
            sys.exit(1)
        nasa.getPublicKey()
        config = nasa.getConfiguration()
        print(config)
        isHost = True if config["host"] == "127.0.0.1" else False
        isPort = True if config["port"] == "8080" else False
        isSystemid = True if config["systemid"] == "systemidtarget" else False
        isComment = isPort = True if config["comment"] == "registered" else False
        isTLS = True if config["tls"] == False else False
        isInterval = True if config["interval"] == 3 else False
        if not isHost or not isPort or not isSystemid or not isComment or not isTLS or not isInterval:
            print("Saved configuration mismatch.")
            sys.exit(1)
        nasa.removeConfiguration()
        print("Test Nasa completed.")

        print("Testing Computer")
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        public_key = key.public_key()
        private_key_pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        public_key_pem = public_key.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)
        computer = Computer(public_key_pem.decode())
        print(computer.getDistribution())
        print(computer.getNetworkUsage())
        print(computer.getDiskIOUsage())
        print(computer.getLocalIPAddress())
        print(computer.getKernelVersion())
        print(computer.getKernelName())
        print(computer.getArchitecture())
        print(computer.getHostname())
        print(computer.getTimedata())
        encrypted = computer.encryptToBase64("TEST STRINg")
        decrypted = key.decrypt(base64.b64decode(encrypted), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        if decrypted.decode() != "TEST STRINg":
            print("Encryption/Decryption ERROR")
        computer.generateSyncData(1)
        time.sleep(1)
        report_SyncDATA = computer.generateSyncData(1)
        report_InformationDATA = computer.generateInformationData()
        print("Test Computer Completed.")

        #print("Testing Rocket")
        #rocket = Rocket("1.1.1.1", "443", False)
        #print(rocket.host)
        #print(rocket.port)
        #rint(rocket.request)
        #print("Test Rocket Completed.")

        print("Testing Pathfinder itself")
        import pathfinder
        pathfinder.deregister()
        pathfinder.default("UNKNOWN")
        pathfinder.default()
        print("Test Pathfinder Completed.")
    except Exception as e:
        traceback.print_exc()
       # sys.exit(1)




