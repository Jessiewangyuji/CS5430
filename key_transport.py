import time
import os
import sys
import subprocess
import pickle

SHA256_LENGTH = 64

DEVNULL = open(os.devnull,'w')

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
    session_key = "Alice" + subprocess.check_output(("openssl", "rand", "64", "-hex"))

    echo_program = subprocess.Popen(('echo',session_key), stdout=subprocess.PIPE)
    session_cipher = subprocess.check_output(("openssl", "rsautl", "-oaep", "-encrypt", "-inkey", "alice/b_public.pem", "-pubin"), stdin=echo_program.stdout)

    message = pickle.dumps([receiver,tA,session_cipher])

    echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
    hashed = subprocess.check_output(("openssl", "dgst", "-sha256"),stdin=echo_program.stdout)[-SHA256_LENGTH-1:].strip()

    echo_program = subprocess.Popen(('echo',hashed), stdout=subprocess.PIPE)
    subprocess.check_output(("openssl", "rsautl", "-sign", "-inkey", "alice/private.pem", "-out", "alice/sig"),stdin=echo_program.stdout)

    digital_signature = read_file("alice/sig")
    os.system("rm alice/sig")

    return pickle.dumps([digital_signature, message]), session_key



def verify_transport_signature(digital_signature_and_message):
    digital_signature, message = pickle.loads(digital_signature_and_message)

    echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
    hashed = subprocess.check_output(("openssl", "dgst", "-sha256"),stdin=echo_program.stdout)[-SHA256_LENGTH-1:]

    write_file("bob/sig",digital_signature)

    hash_to_verify = subprocess.check_output(("openssl", "rsautl", "-verify", "-in", "bob/sig", "-inkey", "bob/a_public.pem", "-pubin"),stderr = DEVNULL)

    os.system("rm bob/sig")

    if hashed == hash_to_verify:
        print("signature verified")
        return pickle.loads(message)

    else:
        print("signature not matched ABORT!")
        return None



# digital_signature_and_message, session_key = sign_session_key("Bob")
# message = verify_transport_signature(digital_signature_and_message)

# print(session_key)
