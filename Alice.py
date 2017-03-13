import socket
import time
import os
import sys
import aes_mac_functions
import key_transport

key = ""
iv = ""

def start_session(socket, receiver, receivehost, receiveport):
    
    digital_signature_and_message, session_key = sign_session_key(receiver)

    sendmsg(socket, digital_signature_and_message, receivehost, receiveport)

    #TODO
    #enc_key = derive_key(session_key,"enc_key")
    #mac_key = derive_key(session_key,"mac_key")


def sendmsg(socket, message, host, port):
    socket.send(message)

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
    print "python Alice.py <configuration> <host> <port>"
    print "configuration: no-cryptography, Enc-only, Mac-only, Enc-then-Mac"
    exit()

host = argv[2]
port = int(argv[3])

action = "y"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver = raw_input("Who do you want to communicate with?")
receivehost = raw_input("What's the host address you want to communicate with?")
receiveport = int(raw_input("What's the port number you want to communicate with?"))
s.connect((receivehost, receiveport))
start_session(s, receiver, receivehost, receiveport)


while action == "y":
    message = raw_input("What's the message you want to send?")
    
    if config == 0:
        final_message = message

    elif config == 1:
        encrypted_message = enc(message,key,iv)
        final_message = iv + encrypted_message

    elif config == 2:
        tag = mac(message,key)
        final_message = tag + message

    elif config == 3:
        tag, encrypted_message = enc_mac(message,key,key,iv)
        final_message = tag + encrypted_message

    sendmsg(s, final_message, receivehost, receiveport)

    action = raw_input("Continue? (y/n)")

s.close()
