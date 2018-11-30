

#Under context supervisor update the publickey into the machine
def updateRemoteRealm(user, publickey, destination):
    print("update ssh realm for the user {0}",user)
    # Add the public keys into the authorised keys 

#Creates the ssh context to let supervisor to access the final system
def createSSHContext(destination):
    return None

#Provision the public key into the machines
def handleRemoteRealm(user, publickey, destinations):
    print("handling user: {0}, destinations:{1}, publicKey: {2}", user, destinations, publickey)

    for dest in destinations:
        #create ssh provision context
        createSSHContext(dest)

        #update the iptables rule to let open the service for that ip

        #update the ssh public key repository into the remote machine
        updateRemoteRealm(user, publickey, dest)
    pass