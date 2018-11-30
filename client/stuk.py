#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import argparse
import socket
from crypto import AE, AD, PairKey, ParsePublicKey
from pnock import Sequences
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

def keyPath(domain, private=False): 
    return ".keys/{0}.{1}.key".format(domain, "private" if private else "public")

def addDomain(domain, path):
    """ Añade las claves creadas sobre el dominio dado """
    with open("{0}/.ssh/config".format(os.getenv("HOME")), "a") as f:
        f.write("Host {0}\n    User cybercamp\n    IdentityFile {1}/{2}\n".format(domain, os.getcwd(), path))

def save(path, stream):
    with open(path, 'bw') as f:
        f.write(stream)

def createLocalRealm(user):
    """ Administra localmente las claves publicas/privadas """
    try:
        print("[] generating keys...")
        publicKey, privateKey = PairKey(plain=True)
        
        save(keyPath(user), publicKey.exportKey('OpenSSH'))
        save(keyPath(user, True), privateKey.exportKey("PEM"))
        
        addDomain(domain, ".key/{0}.private".format(user))
        print("[] ssh configuration saved for user/domain: {0} using {1}...".format(user, ".keys/{0}".format(user)))
        return publicKey
    except Exception as err:
        print("error", err)
        pass
    return None

def createAuthenticationToken(domain, key):
    """ @TODO: work in progress: token must be encrypted using the platform public key """
    return "token#{0}.{1}".format(domain,key)

if __name__ == '__main__':
    #Generamos las claves para el usuario si no existió ( WIP)
    domain = "{0}_{1}".format("user","domain")
    publicKey = createLocalRealm(domain)
    if (publicKey is None):
        exit(-1)

    # Obtener la clave pública proporcionada por la plataforma
    platformKey = ParsePublicKey(".keys/platform.pub")

    # Crear token de autenticación a partir de la clave pública de
    # la plataforma
    token = createAuthenticationToken(domain, platformKey)
    print(token)
    Sequences(sys.argv[1:], token).stuk(destination="10.0.1.137", sequence= [4000,4001,4002])
