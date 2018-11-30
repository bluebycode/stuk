#!/usr/bin/python
from concurrent.futures import ThreadPoolExecutor
from crypto             import OpenPrivateKey
from subprocess         import call
import scapy.all as scapy
import requests

#Platform constants
globals.platformKey = None

#Consumes selected packets per worker
executor = ThreadPoolExecutor(max_workers=10)

#Async. who process the packet by worker
def process(publickey, user, domain, totp, err):
    print(publickey, user, domain, totp, err)
    r = requests.get(constant.AUTH_MOCK_ENDPOINT)
    print(r.text)

# Simple approach to add user into authorisation context
def registerPublicKey(pubkey):
    with open(constant.AUTHORIZED_KEYS_PATH, "a") as auth:
        auth.write(pubkey)

# Packet parser needed for the sniffer
def parser(packet):
    try:
        print(packet.payload)
        token = extractAuthenticationToken(packet.payload)
        if not token:
            return

        publickey, user, domain, totp, err = AD(globals.platformKey, token)
        if (err is not None):
            return
        executor.submit(process())

    except er:
        print("Error", er)

def hook():
    """ Parsing the traffic packets """
    print("[] Listening to device...")
    scapy.sniff(filter='ip proto \\tcp and ((tcp dst port 4000 or 4001 or 4002 or 22) and tcp[tcpflags] & tcp-syn != 0)',prn=parser)

if __name__ == "__main__":
    globals.platformKey = OpenPrivateKey(".keys/platform.key")
    hook()
   