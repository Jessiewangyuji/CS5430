import socket
import time
import os
import sys
from aes_mac_functions import *
from key_transport import *
import datetime

MAX_BYTES_TO_READ = 5000
MAX_TIME_DIFF = 120


#from here: http://stackoverflow.com/questions/13530338/python-comparing-two-times-and-returning-in-minutes
#and here: http://stackoverflow.com/questions/21378977/compare-two-timestamps-in-python
def timeDiff(time1,time2):
    t1 = datetime.datetime.strptime(time1, "%a %b %d %H:%M:%S %Y")
    t2 = datetime.datetime.strptime(time2, "%a %b %d %H:%M:%S %Y")
    return t1 - t2

def establish_session(digital_signature_and_message):
    message = verify_transport_signature(digital_signature_and_message)

    if not message:
        return None

    name = message[0]
    time_sent = message[1]
    session_cipher = message[2]

    if name != "Bob":
        print("incorrect recipient. Abort!")
        return None
    if timeDiff(time.ctime(),time_sent).seconds > MAX_TIME_DIFF:
        print("message too old")
        return None

    write_file("bob/session_cipher.txt",session_cipher)
    
    os.system("openssl rsautl -decrypt -oaep -inkey bob/private.pem -in bob/session_cipher.txt -out bob/session_key.txt")

    return True


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
    
    if not session_established:
        if establish_session(raw_message):
            session_established = True
    else:
        if config == 0:
            print(raw_message)

        elif config == 1:
            iv,message = get_iv_and_message(raw_message)
            print(dec(message,enc_key,iv))

        elif config == 2:
            tag,message = get_tag_and_message(raw_message)
            if(verify_mac(message,hmac_key,tag)):
                print(message)
            else:
                print("HMAC tag did not match. ABORT!")
                exit()

        else:
            tag,encrypted_message = get_tag_and_message(raw_message)
            if(verify_mac(encrypted_message,hmac_key,tag)):
                iv,message = get_iv_and_message(encrypted_message)
                print(dec(message,enc_key,iv))
            else:
                print("HMAC tag did not match. ABORT!")
                exit()


    if action == "n":
        exit()
    action = raw_input("Continue? (y/n)")
clientsocket.close()

   
    

