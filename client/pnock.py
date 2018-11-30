# -*- coding: utf-8 -*-

"""Stuk: Punto de entrada de cliente stuk"""
import socket
import select as select
import time
import sys
import os
import argparse

class Sequences(object):
    def __init__(self, args: list, token):
        print("[] Authentication token: {0}".format(token))
        self._parse_args(args)

    def _parse_args(self, args: list):
        parser = argparse.ArgumentParser()
        
        parser.add_argument('destination', help='IP address of destination')
        parser.add_argument('token', help='TOTP')
        
        args = parser.parse_args(args)
        print("destination",args.destination)
        print("token",args.token)
        
        self.address, _, _, _, (self.destination, _) = socket.getaddrinfo(
                host="10.0.1.135",
                port=22,
                flags=socket.AI_ADDRCONFIG)[0]

    def stuk(self, destination, sequence = [4000,4001,4002]):
        for nth, port in enumerate(sequence):
            peer = socket.socket(self.address, socket.SOCK_STREAM)
            peer.setblocking(False)
            address = (destination, int(port))
            peer.connect_ex(address)
            if (nth is len(sequence) - 1):
                peer.send(b"AAAAAAAAAAAAAAAA")
            select.select([peer], [peer], [peer], 10000)

            peer.close()
            time.sleep(0.5)