import socket
import time
import os
import sys

def start_session(socket, receiver, receivehost, receiveport):
    tA = time.localtime()
    os.system("openssl rand 128 > session_symmetric.txt")
    with open("session_symmetric.txt", "r") as file:
        session_key = file.read()
    print session_key
    os.system("openssl ")

def sendmsg(socket, message, host, port):
    socket.send(message.encode('utf-8'))

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

if config == 0:
    action = "y"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver = raw_input("Who do you want to communicate with?")
    receivehost = raw_input("What's the host address you want to communicate with?")
    receiveport = int(raw_input("What's the port number you want to communicate with?"))
    s.connect((receivehost, receiveport))
    #start_session(s, receiver, receivehost, receiveport)
    while action == "y":
        message = raw_input("What's the message you want to send?")
        sendmsg(s, message, receivehost, receiveport)
        action = raw_input("Continue? (y/n)")
    s.close()
elif config == 1:
    enc(host, port)
elif config == 2:
    mac(host, port)
else:
    enc_mac(role, host, port)


