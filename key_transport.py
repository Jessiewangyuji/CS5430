import time
import os
import sys
import subprocess
import pickle

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

    tA = time.ctime()
    os.system("openssl rand 64 -hex -out alice/session_key.txt")
    session_key = read_file("alice/session_key.txt")

    os.system("openssl rsautl -oaep -encrypt -inkey alice/b_public.pem -pubin -in alice/session_key.txt -out alice/session_cipher.txt")

    session_cipher = read_file("alice/session_cipher.txt")

    message = pickle.dumps([receiver,tA,session_cipher])

    write_file("alice/message.txt",message)

    hashed = subprocess.check_output(("openssl", "dgst", "-sha256", "alice/message.txt"))[-SHA256_LENGTH-1:]

    write_file("alice/hashed.txt",hashed)

    os.system("openssl rsautl -sign -in alice/hashed.txt -inkey alice/private.pem -out alice/sig")

    digital_signature = read_file("alice/sig")

    return pickle.dumps([digital_signature, message]), session_key



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





# digital_signature_and_message, session_key = sign_session_key("Bob")
# message = verify_transport_signature(digital_signature_and_message)

# print(session_key)
