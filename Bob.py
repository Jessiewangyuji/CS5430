import socket
import time
import os
import sys
import aes_mac_functions

HMAC_TAG_LENGTH = 64
IV_LENGTH = 32


def establish_session(message):
    print message
    with open("bob/session_cipher.txt", "w+") as file:
        file.write(message.strip())
        file.close()
    
    os.system("openssl rsautl -decrypt -inkey bob/private.pem -in bob/session_cipher.txt -out bob/decrypted_session.txt")

    with open("bob/decrypted_session.txt", "r") as file:
        content = file.readlines()
        file.close()
    content = [x.strip() for x in content]
    print content[0]
    intended = content[0]
    time = content[1]
    kAB = content[2]

    print intended, time, kAB
    if intended != "B":
        print "message intended for ", intended, ". Abort"
        exit()
    localtime = time.ctime
    if localtime - time.ctime(time) > 1000:
        print "time diff, abort"




argv = sys.argv
config = argv[1]

session_established = False

if config == "no-cryptography":
    config = 0
elif config == "Enc-only":
    config = 1
elif config == "Mac-only":
    config = 2
elif config == "Enc-then-Mac":
    config = 3
else:
    print "python Bob.py <configuration> <host> <port>"
    print "configuration: no-cryptography, Enc-only, Mac-only, Enc-then-Mac"
    exit()

host = argv[2]
port = int(argv[3])

action = "y"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
(clientsocket, address) = s.accept()

while action == "y":
    raw_message = clientsocket.recv(5000)

    if config == 0:
        print(raw_message)
    elif config == 1:
        iv = raw_message[:IV_LENGTH]
        message = raw_message[IV_LENGTH:]
        print(dec(message,enc_key,iv))
    elif config == 2:
        tag = raw_message[:HMAC_TAG_LENGTH]
        message = raw_message[HMAC_TAG_LENGTH:]
        if(verify_mac(message,hmac_key,tag)):
            print(message)
        else:
            print("HMAC tag did not match")
    else:
        tag = raw_message[:HMAC_TAG_LENGTH]
        mac_message = [HMAC_TAG_LENGTH:]
        if(verify_mac(mac_message,hmac_key,tag)):
            iv = mac_message[:IV_LENGTH]
            message = mac_message[IV_LENGTH:]
            print(dec(message,enc_key,iv))
        else:
            print("HMAC tag did not match")


    if not session_established:
        establish_session(message)
    action = raw_input("Continue?(y/n)")
    if action == "n":
        exit()


   
    

