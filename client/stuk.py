#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import argparse
import socket
from crypto import AE, AD, PairKey
from Crypto.PublicKey import RSA
import select as select
import time
import sys
import os

class Authentication(object):
    def build(self):
        token = AE("tests/.keys/it_public.pem", "AAAAAAAAA")
        print("[] encrypted token {0}".format(token))
        decrypted = AD("tests/.keys/it_private.pem", token)
        print("[] decrypted token {0}".format(decrypted))
        return "AAAAAAAAA"

class Sequences(object):
    def __init__(self, args: list, token):
        print("[] Authentication token", token)
        self._parse_args(args)

    def _parse_args(self, args: list):
        parser = argparse.ArgumentParser()
        parser.add_argument('destination', help='IP address of destination')
        parser.add_argument('token', help='TOTP')

        args = parser.parse_args(args)
        
        self.address, _, _, _, (self.destination, _) = socket.getaddrinfo(
                host="10.0.1.135",
                port=22,
                flags=socket.AI_ADDRCONFIG
            )[0]
    def stuk(self):
        for port in [4000,4001,4002]:
            peer = socket.socket(self.address, socket.SOCK_STREAM)
            peer.setblocking(False)
            address = ("10.0.1.135", int(port))
            peer.connect_ex(address)
            select.select([peer], [peer], [peer], 10000)
            peer.close()
            time.sleep(0.5)

def addDomain(domain, path):
    with open("{0}/.ssh/config".format(os.getenv("HOME")), "a") as f:
        f.write("Host {0}\n    User cybercamp\n    IdentityFile {1}/{2}\n".format(domain, os.getcwd(), path))
        
def save(path, stream):
    with open(path, 'bw') as f:
        f.write(stream)

def createLocalRealm(user, domain):
    try:
        publicKey, privateKey = PairKey(plain=True)
        print(publicKey, privateKey)
        save(".keys/{0}_{1}.public".format(user,domain), publicKey.exportKey('OpenSSH'))
        save(".keys/{0}_{1}.private".format(user,domain), privateKey.exportKey("PEM"))
        addDomain(domain, ".key/{0}_{1}.private".format(user,domain))
        return user+"/"+domain, publicKey
    except Exception as err:
        print("error", err)
        pass
    return None,None

def createAuthenticationToken(domain, key):
    return "{0}.{1}".format(domain,key)

if __name__ == '__main__':
    domainToken, publicKey = createLocalRealm("user", "domain.org")
    if (domainToken is None):
        exit(-1)
    Sequences(sys.argv[1:], createAuthenticationToken(domainToken, publicKey)).stuk()
