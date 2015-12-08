from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import random
import string
import os

def gen_cipher():
	r = Random.new()
	key = r.read(32)
	with open("AES_Key.txt", 'wb') as f:
		f.write(key)