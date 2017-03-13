import socket
import time
import os
import sys
import aes_mac_functions

key = ""
iv = ""

def start_session(socket, receiver, receivehost, receiveport):
    print "start_session"
    tA = time.ctime()
    os.system("openssl rand 128 > alice/session_symmetric.txt")
    #os.system("openssl rand 128 > alice/session_iv.txt")
    with open("alice/session_symmetric.txt", "r") as file:
        session_key = file.read()
        global key
        key = session_key
        file.close()
    """with open("alice/session_iv.txt", "r") as file:
        session_iv = file.read()
        global iv
        iv = session_iv
        file.close()"""
    print session_key
    with open("alice/session_key.txt", "w+") as file:
        file.write(receiver + "\n" + tA + "\n" + session_key)
        file.close()

    os.system("openssl rsautl -encrypt -inkey alice/b_public.pem -pubin -in alice/session_key.txt -out alice/session_cipher.txt")

    with open("alice/session_cipher.txt", "r") as file:
        sign = file.read()
        file.close()

    sign = receiver + "\n" + tA + "\n" + sign

    print "sign: ", sign

    with open("alice/sign.txt", "w+") as file:
        file.write(sign)
        file.close()

#os.system("openssl rsautl -sign -in alice/sign.txt -inkey alice/private.pem -out alice/sig")


    with open("alice/session_cipher.txt", "r") as file:
        session_cipher = file.read().strip()
        file.close()

#with open("alice/sig", "r") as file:
#        session_cipher = session_cipher + file.read().strip()
#        file.close()

    sendmsg(socket, session_cipher, receivehost, receiveport)

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
