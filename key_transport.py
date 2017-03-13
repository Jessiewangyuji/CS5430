import socket
import time
import os
import sys
import subprocess
import pickle
import datetime

SHA256_LENGTH = 64


def read_file(filename):
    temp = ""
    with open(filename,"r") as file:
        temp = file.read()
        file.close()
    return temp

def write_file(filename,data):
    with open(filename,"w") as file:
        file.write(data)
        file.close()


def sign_session_key(receiver):
    print "start_session"

    # session_key_file = "/session_key.txt"
    # receiver_public_file = "/b_public.pem"
    # session_cipher_file = "/session_cipher.txt"
    # message_file = "/message.txt"
    # hashed_file = "/hashed.txt"
    # sender_private_file = "/private.pem"
    # signature_file = "sig"

    tA = time.ctime()
    os.system("openssl rand 64 -hex -out alice/session_key.txt")
    with open("alice/session_key.txt", "r") as file:
        session_key = file.read()
        global key
        key = session_key
        file.close()

    print(len(session_key))

    os.system("openssl rsautl -oaep -encrypt -inkey alice/b_public.pem -pubin -in alice/session_key.txt -out alice/session_cipher.txt")

    session_cipher = read_file("alice/session_cipher.txt")

    message = pickle.dumps([receiver,tA,session_cipher])

    write_file("alice/message.txt",message)

    hashed = subprocess.check_output(("openssl", "dgst", "-sha256", "alice/message.txt"))[-SHA256_LENGTH-1:]
    print(hashed)

    write_file("alice/hashed.txt",hashed)

    os.system("openssl rsautl -sign -in alice/hashed.txt -inkey alice/private.pem -out alice/sig")

    digital_signature = read_file("alice/sig")

    return pickle.dumps([digital_signature, message])



def verify_transport_signature(digital_signature_and_message):
    digital_signature, message = pickle.loads(digital_signature_and_message)

    write_file("bob/sig",digital_signature)
    write_file("bob/message.txt",message)

    hashed = subprocess.check_output(("openssl", "dgst", "-sha256", "bob/message.txt"))[-SHA256_LENGTH-1:]

    write_file("bob/hashed.txt",hashed)

    hash_to_verify = subprocess.check_output(("openssl", "rsautl", "-verify", "-in", "bob/sig", "-inkey", "bob/a_public.pem", "-pubin"))

    if hashed == hash_to_verify:
        print("signature verified")
        return pickle.loads(message)

    else:
        print("signature not matched ABORT!")
        return None





# digital_signature_and_message = sign_session_key("Bob")
# message = verify_transport_signature(digital_signature_and_message)
