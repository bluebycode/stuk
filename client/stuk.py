#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import argparse
import socket
from pnock import Sequences, getLocalIP
import crypto
import time
import sys
import os
import zlib
import base64
import json
import constant

def createAuthenticationToken(user, domain, totp, key, encryption=True):
    """ Creates the authentication token encrypted and ready to send """
    with open(constant.USER_PUBLIC_KEY.format(user), "r") as f:
        publicToken = f.read()
        token = bytes("{0};{1};{2};{3}".format(user,domain,totp, publicToken), 'utf8')
        if (encryption):
            return crypto.AE(constant.PLATFORM_KEY, token)
        else:
            return base64.b64encode(zlib.compress(token))
            
def addDomain(user, domain, path):
    """ Append the keys into the ssh configuration """
    with open("{0}/.ssh/config".format(os.getenv("HOME")), "a") as f:
        f.write("Host {0}\n    User {1}\n    IdentityFile {2}/{3}\n".format(domain, user.split("@")[0], os.getcwd(), path))

def save(path, stream):
    with open(path, 'bw') as f:
        f.write(stream)

def createLocalRealm(user, domain):
    """ Administra localmente las claves publicas/privadas """
    try:
        print("[] Generating pair keys...")
        publicKey, privateKey = crypto.PairKey(plain=True)
        print("[] Saving keys ...")
        save(constant.USER_PUBLIC_KEY.format(user), publicKey.exportKey('OpenSSH'))
        os.chmod(constant.USER_PUBLIC_KEY.format(user), 0o600)
        save(constant.USER_PRIVATE_KEY.format(user), privateKey.exportKey("PEM"))
        
        print("[] adding local configuration ...")
        addDomain(user, domain, constant.USER_PRIVATE_KEY.format(user))
        print("[] ssh configuration saved for user/domain: {0} using {1}...".format(user, ".keys/{0}".format(user)))
        return publicKey
    except Exception as err:
        print("error", err)
        pass
    return None

def parseArgumentProfile():
    """ Loading the preferences from profile file """
    profile = json.loads(open(constant.PROFILE_DEFAULT_LOCATION).read())
    return (profile["email"], profile["ip"])

if __name__ == '__main__':
    totp_argument = 1
    (user, destination) = parseArgumentProfile()
    if (user is None):
        user  = argv[1]
        destination = argv[2]
        totp_argument = 3

    # default sequence
    sequence = [4000,4001,4002,4003]

    #it generates the keys if not exists
    publicKey = createLocalRealm("{0}_{1}".format(user, constant.DOMAIN), destination)
    if (publicKey is None):
        exit(-1)

    # TOTP
    totp = sys.argv[totp_argument]
    print("[] received one time password: ", totp)

    #domain
    print("[] destination: ", destination)
    print("[] user/domain: ", user, constant.DOMAIN)

    #use the platform public
    platformKey = crypto.ParsePublicKey(constant.PLATFORM_KEY)
    print("[] Clave de plataforma {0}".format(platformKey))

    #creates the authentication token by the platform public
    token = createAuthenticationToken(user, constant.DOMAIN, totp, platformKey)

    #Sending the port knocking sequence
    print("[] Sending Token: {0} under the sequence: {1}".format(token,sequence))
    sequences = Sequences(getLocalIP(), destination,token)
    sequences.send(sequence=sequence)
    print("[] Done.")
