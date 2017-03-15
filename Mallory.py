import socket
import time
import os
import sys
import pickle

def sendmsg(socket, message, host, port):
    socket.send(message)

def replay():
    print "replay"


def print_message(raw_message,config):

    message_num = None
    message = None
    iv = None
    ciphertext = None
    tag = None

    if config == 0:
        message_num = raw_message.split(" ")[0]
        print "Message: ",raw_message 
    elif config == 1:
        iv,ciphertext = pickle.loads(raw_message)
        print "Ciphertext: ", ciphertext
    elif config == 2:
        tag,message = pickle.loads(raw_message)
        print "HMAC tag: ", tag
        print "Message: ", message
    elif config == 3:
        tag,encrypted = pickle.loads(raw_message)
        iv,ciphertext = pickle.loads(encrypted)
        print "HMAC tag: ", tag 
        print "Ciphertext: ", ciphertext

    return message_num,message,iv,ciphertext,tag

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

receivehost = raw_input("What's the host address you want to communicate with?")
receiveport = int(raw_input("What's the port number you want to communicate with?"))

action = "y"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
(clientsocket, address) = s.accept()

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((receivehost, receiveport))

while action == "y":
    raw_message = clientsocket.recv(5000)
    # print clientsocket.gettimeout()
    message_num,message,iv,ciphertext,tag = print_message(raw_message,config)

    counter += 1
    if raw_input("Save?(y/n)") == 'y':
        filename = "mallory/message" + str(counter) + ".txt"
        with open(filename, "w+") as file:
            file.write(raw_message)
            file.close()

    action2 = raw_input("What do you want to do with the message?(forward, delete, modify, replay)")

    if action2 == "forward":
        sendmsg(s2, raw_message, receivehost, receiveport)

    elif action2 == "modify":
        print "modify"
        new_message = raw_input("What do you want to modify the message to?")
        if message_num != None:
            new_message = message_num + " " + new_message
        if config == 0:
            raw_message = new_message

        elif config == 1:
            raw_message = pickle.dumps([iv,new_message])

        elif config == 2:
            raw_message = pickle.dumps([tag,new_message])

        elif config == 3:
            raw_message = pickle.dumps([tag,pickle.dumps([iv,new_message])])

        sendmsg(s2, raw_message, receivehost, receiveport)
    elif action2 == "delete":
        print raw_message, " deleted"
    elif action2 == "replay":
        filename = raw_input("Which message to replay?")
        with open(filename, "r") as file:
            raw_message = file.read()
            file.close()
        sendmsg(s2, raw_message, receivehost, receiveport)


    action = raw_input("Continue?(y/n)")

    
clientsocket.close()
s2.close()


