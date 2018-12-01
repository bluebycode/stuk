# -*- coding: utf-8 -*-

"""Stuk: Port-Knocking implementation"""
import socket
import select as select
import time
import sys
import os
import constant

def getLocalIP():
    return constant.LOCAL_IP

class Sequences(object):
    def __init__(self, source, destination, token):
        print("[] Authentication token: {0}".format(token))
        self.source = source
        self.destination = destination
        self.token = token

    def send(self, sequence = [4000,4001,4002], timeFrame = 5, ramp = 0.5):
        print("[] Sending the sequence.. {0}".format(sequence))
        if constant.DEBUG:
            print(self.destination, sequence, self.token)

        #Getting ready the address
        address_family, _, _, _, (address_ip, _) = socket.getaddrinfo(
            host=self.destination,
            port=sequence[0],
            flags=socket.AI_ADDRCONFIG
            )[0]
        #Sending the sequence
        for nth, port in enumerate(sequence):
            sock = socket.socket(address_family, socket.SOCK_STREAM)
            sock.setblocking(False)
            socket_address = (address_ip, int(port))
            sock.connect_ex(socket_address)
            #select.select([sock], [sock], [sock], 2000)
            time.sleep(ramp)
            sock.close()            
        time.sleep(timeFrame)
        #Windows is open!
        usock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        usock.sendto(self.token, (address_ip, sequence[len(sequence)-1]))
        usock.close()