#!/usr/bin/python
import scapy.all as scapy
from subprocess import call
from concurrent.futures import ThreadPoolExecutor
import requests
import base64
import zlib
import requests
import json
import paramiko
import thread
import remote
import constant
import crypto

#consumes selected packets per worker
executor = ThreadPoolExecutor(max_workers=10)

#simple approach to add user into authorisation context
def PublicKey(pubkey):
    with open(constant.AUTHORIZED_KEYS_PATH, "a") as auth:
        auth.write(pubkey)

def tcpParser(name, ref):
  print("tcp listening...")
  scapy.sniff(iface="ens37",filter='ip proto \\tcp and ((tcp dst port 4000 or 4001 or 4002 or 4003 or 4004 or 22) and tcp[tcpflags] & tcp-syn != 0)',prn=tcpparser)

def udpParser(name, ref):
  print("udp listening...")
  scapy.sniff(iface="ens37",filter='ip proto \\udp and ((udp dst portrange 4000-4100))',prn=udpparser)

sequences = {}
queue = {}

def checksum(sequence):
  print("checksum:", sequence)

def handleDecryptedData(decrypted):
  try:
    token = provision(decrypted)
    if not token:
      return
  except Exception as er:
    print("Error", er)

def processUdp(sourceIp, decrypted,lastSequence):
  print("sequence udp got!",sourceIp, decrypted,lastSequence)
  if queue.has_key(sourceIp):
    del queue[sourceIp]
    checksum(lastSequence)
    print("allowed")
    handleDecryptedData(decrypted)
  else:
    print("not allowed",sourceIp)

def processTcp(sourceIp, lastSequence):
  print("sequence tcp got!",sourceIp, lastSequence)
  queue[sourceIp]=lastSequence
  if checksum(lastSequence):
      open_time_window(ssh)

# Packet parser needed for the sniffer
def udpparser(packet):
    try:
        print("UDP >>>",packet.payload.payload,packet.payload.src)
        source = packet.payload.src
        encrypted_token=packet.payload.payload.load
        print("data",encrypted_token)
        decrypted = crypto.AD(".keys/plataforma.pem",encrypted_token)
        executor.submit(processUdp(source,decrypted,"1"))
    except Exception as er:
        print("Error", er)

def ssh_append(ssh, publicKey):
    ftp = ssh.open_sftp()
    print("Appending ", constant.AUTHORIZED_KEYS_PATH)
    file=ftp.file(constant.AUTHORIZED_KEYS_PATH, "a", -1)
    file.write("{0}\n".format(publicKey))
    file.flush()
    ftp.close()

#https://codereview.stackexchange.com/questions/171179/python-script-to-execute-a-command-using-paramiko-ssh
def ssh_command(ssh, command, publicKey):
    ssh.invoke_shell()
    _, stdout, _ = ssh.exec_command("hostname")
    print(stdout.read())
    print("Command:", command)
    _, stdout, _ = ssh.exec_command(command)
    print(stdout.read())
    ssh_append(ssh, publicKey)

def open_time_window(port=4003):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=destination, username="cybercamp",
            key_filename=constant.SUPERVISOR_KEY)
        ssh.invoke_shell()
        _, stdout, _ = ssh.exec_command("hostname")
        print(stdout.read())
        print("Command:", command)
        _, stdout, _ = ssh.exec_command('iptables  -A INPUT  -p udp --dport 4003 -s 100.0.1.0/24 -m comment --comment "expire=`date -d '+ 5 min' +%s`" -j ACCEPT ')
        print(stdout.read())
        print(user, destination)
    except Exception as e:
        print('Connection Failed',e)
        print(e)
    
def handlePublicKey(publicKey, user, destination):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=destination, username="cybercamp",
            key_filename=constant.SUPERVISOR_KEY)
        ssh_command(ssh, "adduser {0}".format(user), publicKey)
        print(user, destination)
    except Exception as e:
        print('Connection Failed',e)
        print(e)


def provision(token, default_destination="10.0.1.139"):
    """['zel@uma.es', 'zel', '23232', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCdQ0AJqWQELL2IhRPA3BrpJvUzYRbpMKJymReDaeUyLPT+L17fPxXMw6MyFpJAxNQ0059xnSZUKPH/onQDI2hLjzV0Qh91VlKDv/ZDFcB2mHj6PULMfJGhiJ2tfq/HMW53pflpwGxd+lmKr7AJZ0kDQdVed+a2r44kWIVtPtgQGYLahoJ11obZCB7vApMOjDuldzzNEWIWTc8tIWBQg60EtDno4kn8BCRnEeYoVTpmCDtALA1HOXYD8PIJkRE8MH7qyqDoCCohb2/uBJsDlUt3ASmHy5hSkQDj0zq7g57/NgQTs6vlJYvnFlJBYd60yaMMqpC2CLIpK8Cf0C18RP2L'])
    """
    try:
        tokens = token.split(";")
        print("Token to extract", token.split(";"))
        user = tokens[0]
        key  = tokens[1]
        totp = tokens[2]
        publickey = tokens[3]
        r = requests.get(constant.VERIFICATION_PATH.format(base64.b64encode(user+";"+key+";"+totp+";" + default_destination)))
        print(r.text,json.loads(r.text))
        response = json.loads(r.text)
        verify = response['verify']
        machine_user = response['machine_user']
        if verify is not True:
           return None
        domain = user.split("@")[1]
        handlePublicKey(publickey+ " " + machine_user + "@" + domain, machine_user, default_destination)
    except Exception as e:
        print('Token extraction failed',e)
        print(e)

def tcpparser(packet):
    try:
        print("TCP >>>",packet.payload.payload,packet.payload.src)
        source = packet.payload.src
        seq = packet.payload.payload.dport
        num = sequences.get(source)
        sequences[source]=1 if num is None else num + 1
        print(source,num)
        if (num >= 2):
          executor.submit(processTcp(source,seq))

    except Exception as er:
        print("Error", er)

def hook():
    """ Parsing the traffic packets """
    print("[] Listening to device...")
    try:
      thread.start_new_thread(tcpParser, ("tcp-filter", 2))
      thread.start_new_thread(udpParser, ("udp-filter", 4))
    except Exception as er:
      print("Error: unable to start thread",er)

    while 1:
      pass

if __name__ == "__main__":

    hook()