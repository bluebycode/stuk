import zlib
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def PairKey(plain=False):
    key = RSA.generate(2048)
    return (key, key.publickey()) if plain else (key.exportKey("PEM"), key.publickey().exportKey('OpenSSH'))

def AD(rsa, cipheredmessage):
    """ RSA - Asymetric Decryptation mediante PKCS1_OAEP """
    key = RSA.importKey(open(rsa).read())
    cipher = PKCS1_OAEP.new(key)
    block = 256
    offset = 0
    encrypted = base64.b64decode(cipheredmessage)
    decrypted=b""
    while offset < len(encrypted):
        chunk = encrypted[offset:offset + block]
        print(len(chunk))
        decrypted+= cipher.decrypt(chunk)
        offset+=block
    return decrypted

def AE(rsa, message):
    """ RSA - Asymetric Encriptation mediante PKCS1_OAEP """
    key = RSA.importKey(open(rsa).read())
    cipher = PKCS1_OAEP.new(key)
    #message = zlib.compress(message)
    block=128
    offset=0
    blocks=True
    encrypted=b""
    while blocks:
        chunk = message[offset:offset + block]
        if len(chunk) % block !=0:
            blocks=False
            chunk +=b'.' * (block - len(chunk))
        encrypted+=cipher.encrypt(chunk)
        offset+=len(chunk)
    return base64.b64encode(encrypted)
