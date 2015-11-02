__author__ = 'adminuser'

import os
from Crypto.PublicKey import RSA
from Crypto import Random

if "PrivateKey.txt" not in os.listdir(os.getcwd()):
    r = Random.new().read
    key = RSA.generate(4096, r)
    with open("PrivateKey.txt", "w") as f:
        f.write(key.exportKey(format="PEM", pkcs=8).decode())
    with open("PublicKey.txt", "w") as f:
        f.write(key.publickey().exportKey(format="PEM", pkcs=1).decode())
