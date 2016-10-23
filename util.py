import base64
import random
from string import hexdigits

from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length) * length


def unpad(data):
    return data[:-ord(data[-1])]


def generate_string(length=32, alpha=hexdigits):
    characters = [random.choice(alpha) for x in range(length)]
    return "".join(characters)


def decrypt(ciphertext, key):
    encrypted = base64.b64decode(ciphertext)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(key, AES.MODE_CBC, IV)
    return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))


def encrypt(message, key):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, IV)
    return base64.b64encode(IV + aes.encrypt(pad(message)))
