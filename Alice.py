import socket
import time
import os
import sys

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

    os.system("openssl rsautl -sign -in alice/session_cipher.txt -inkey alice/private.pem -out alice/sig")


    with open("alice/session_cipher.txt", "r") as file:
        session_cipher = file.read().strip()
        file.close()

    with open("alice/sig", "r") as file:
        session_cipher = session_cipher + file.read().strip()
        file.close()

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
    start_session(s, receiver, receivehost, receiveport)
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


