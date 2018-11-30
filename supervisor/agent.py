agent.py#!/usr/bin/python
from concurrent.futures import ThreadPoolExecutor
from crypto             import OpenPrivateKey
from subprocess         import call
from provision          import handleRemoteRealm
import scapy.all as scapy
import requests
import constant

#Platform constants
globals.platformKey = None

#Consumes selected packets per worker
executor = ThreadPoolExecutor(max_workers=10)

#Async. who process the packet by worker
def process(publickey, user, destinations, totp, err):
    print(publickey, user, destinations, totp, err)
    r = requests.get(constant.AUTH_MOCK_ENDPOINT)

    if r.text.result is "200":
        handleRemoteRealm(user, publickey, destinations)

    print(r.text)

# Simple approach to add user into authorisation context
def registerPublicKey(pubkey):
    with open(constant.AUTHORIZED_KEYS_PATH, "a") as auth:
        auth.write(pubkey)

# Extraction of authentication token from tcp packet
def extractAuthenticationToken(payload):
    """ @todo: extract/parse from packet the encrypted block stream """
    if not payload:
        return None
    return b"AAAAAAA"

# Packet parser needed for the sniffer
def parser(packet):
    try:
        print(packet.payload)
        token = extractAuthenticationToken(packet.payload)
        if not token:
            return

        #Decrypt the token and obtains the tuple of honor
        publickey, user, destinations, totp, err = AD(globals.platformKey, token)
        if (err is not None):
            return
        executor.submit(process(publickey, user, destinations, totp, err))

    except er:
        print("Error", er)

def hook():
    """ Parsing the traffic packets """
    print("[] Listening to device...")
    scapy.sniff(filter=constant.DEFAULT_FILTER_SEQUENCE, prn=parser)

if __name__ == "__main__":
    globals.platformKey = OpenPrivateKey(constant.PLATFORM_KEYS_PATH)
    hook()
   
