#!/usr/bin/python
import scapy.all as scapy
from subprocess import call
import concurrent.futures

# Consumes selected packets per worker 
executor = ThreadPoolExecutor(max_workers=10)

# Async. who process the packet by worker
def process(publickey, user, domain, totp, err):
    print(publickey, user, domain, totp, err)

# Simple approach to add user into authorisation context
def registerPublicKey(pubkey):
    with open("/home/osboxes/.ssh/.authorizedkeys", "a") as auth:
        auth.write(pubkey)

# Packet parser needed for the sniffer
def parser(packet):
    try:
        print(packet.payload)
        token = extractAuthenticationToken(packet.payload)
        if not token:
            return

        publickey, user, domain, totp, err = encrypt(token)
        if (err is not None):
            return
        executor.submit(process())
        
    except er:
        print("Error", er)

def parseTraffic():
    """ Parsing the traffic packets """ 
    print("[] Listening to device...")
    scapy.sniff(filter='ip proto \\tcp and ((tcp dst port 4000 or 4001 or 4002 or 22) and tcp[tcpflags] & tcp-syn != 0)',prn=parser)

if __name__ == "__main__":
    parse()