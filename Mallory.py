import socket
import time
import os
import sys

def sendmsg(socket, message, host, port):
    socket.send(message)

def replay():
    print "replay"

argv = sys.argv
config = argv[1]

if config == "no-cryptography":
    config = 0
elif config == "Enc-only":
    config = 1
elif config == "Mac-only":
    config = 2
elif config == "Enc-then-Mac":
    config = 3
else:
    print "Python Alice.py <configuration> <host> <port>"
    print "configuration: no-cryptography, Enc-only, Mac-only, Enc-then-Mac"
    exit()

host = argv[2]
port = int(argv[3])
counter = 0


action = "y"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
(clientsocket, address) = s.accept()

receivehost = raw_input("What's the host address you want to communicate with?")
receiveport = int(raw_input("What's the port number you want to communicate with?"))
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((receivehost, receiveport))

while action == "y":
    message = clientsocket.recv(5000)
    print clientsocket.gettimeout()
    counter += 1
    print message
    if raw_input("Save?(y/n)") == 'y':
        filename = "mallory/message" + str(counter) + ".txt"
        with open(filename, "w+") as file:
            file.write(message)
            file.close()

    action2 = raw_input("What do you want to do with the message?(forward, delete, modify, replay)")
    if action2 == "forward":
        sendmsg(s2, message, receivehost, receiveport)
    elif action2 == "modify":
        print "modify"
        message = raw_input("What do you want to modify the message to?")
        sendmsg(s2, message, receivehost, receiveport)
    elif action2 == "delete":
        print message, " deleted"
    elif action2 == "replay":
        filename = raw_input("Which message to replay?")
        with open(filename, "r") as file:
            message = file.read()
            file.close()
        sendmsg(s2, message, receivehost, receiveport)


    action = raw_input("Continue?(y/n)")
#TODO: Change receiver
    
clientsocket.close()
s2.close()


