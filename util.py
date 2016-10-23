import base64
import random
from string import hexdigits


def generate_string(length=32, alpha=hexdigits):
    characters = [random.choice(alpha) for x in range(length)]
    return "".join(characters)


def decrypt(ciphertext, aes):
    return aes.decrypt(base64.b64decode(ciphertext))


def encrypt(message, aes):
    return aes.encrypt(message)
