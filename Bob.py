import socket
import time
import os
import sys
from aes_mac_functions import *
from key_transport import *
import datetime
import pickle
import subprocess

MAX_BYTES_TO_READ = 5000
MAX_TIME_DIFF = 120

enc_key = ""
mac_key = ""

#from here: http://stackoverflow.com/questions/13530338/python-comparing-two-times-and-returning-in-minutes
#and here: http://stackoverflow.com/questions/21378977/compare-two-timestamps-in-python
def timeDiff(time1,time2):
    t1 = datetime.datetime.strptime(time1, "%a %b %d %H:%M:%S %Y")
    print t1
    t2 = datetime.datetime.strptime(time2, "%a %b %d %H:%M:%S %Y")
    print t2
    return t1 - t2

def establish_session(digital_signature_and_message):
    message = verify_transport_signature(digital_signature_and_message)

    if not message:
        return False

    name = message[0]
    time_sent = message[1]
    session_cipher = message[2]

    if name != "Bob":
        print "incorrect recipient. Abort!"
        return False
    if timeDiff(time.ctime(),time_sent).seconds > MAX_TIME_DIFF:
        print "message too old" 
        return False

    write_file("bob/session_cipher.txt",session_cipher)
    
    session_key = subprocess.check_output(("openssl", "rsautl", "-decrypt", "-oaep", "-inkey", "bob/private.pem", "-in", "bob/session_cipher.txt"))
    name = session_key[:5]
    session_key = session_key[5:]

    if name != "Alice":
        print "Sender is not Alice"
        return False

    os.system("rm bob/session_cipher.txt")

    enc_key = derive_key(session_key,"enc_key")
    mac_key = derive_key(session_key,"mac_key")

    return True


argv = sys.argv
config = argv[1]

session_established = False
messageNo = 0
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

receivedNo = 0

while action == "y":
    raw_message = clientsocket.recv(5000)
    
    if not session_established:
        if establish_session(raw_message):
            session_established = True
            continue
    else:
        if config == 0:
            print raw_message 
            receivedNo = raw_message.split(" ")[0]

        elif config == 1:
            [iv,message] = pickle.loads(raw_message)
            try:
                dec_message = dec(message,enc_key,iv)
                receivedNo = dec_message.split(" ")[0]
                print dec_message
            except:
                print "decrypt failed!"


        elif config == 2:
            [tag,message] = pickle.loads(raw_message)
            if(verify_mac(message,mac_key,tag)):
                print message
            else:
                print "HMAC tag did not match. ABORT!"
                exit()
            receivedNo = message.split(" ")[0]

        else:
            [tag,encrypted_message] = pickle.loads(raw_message)
            if(verify_mac(encrypted_message,mac_key,tag)):
                [iv,message] = pickle.loads(encrypted_message)
                dec_message = dec(message,enc_key,iv)
                print dec_message
            else:
                print "HMAC tag did not match. ABORT!"
                exit()
            receivedNo = dec_message.split(" ")[0]
                
        if int(receivedNo) != messageNo:
            print "Message number mismatch. Possible Replay Attack! Abort"
            exit()
        else:
            messageNo += 1

    if action == "n":
        exit()
    action = raw_input("Continue? (y/n)")
clientsocket.close()

   
    

