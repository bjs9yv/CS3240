__author__ = 'adminuser'
from Crypto.PublicKey import RSA
from Crypto import Random

def gen_keys():
    r = Random.new().read
    key = RSA.generate(4096, r)
    # TODO: store keys in a subdirectory not current directory
    with open("PrivateKey.txt", "w") as f:
        f.write(key.exportKey(format="PEM", pkcs=8).decode())
    with open("PublicKey.txt", "w") as f:
        f.write(key.publickey().exportKey(format="PEM", pkcs=1).decode())