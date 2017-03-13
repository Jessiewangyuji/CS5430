import socket
import time
import os
import sys
import subprocess


SHA256_LENGTH = 64



def sign_session_key(receiver):
    print "start_session"
    tA = time.ctime()
    os.system("openssl rand 64 -hex -out alice/session_key.txt")
    with open("alice/session_key.txt", "r") as file:
        session_key = file.read()
        global key
        key = session_key
        file.close()

    print session_key

    os.system("openssl rsautl -oaep -hexdump -encrypt -inkey alice/b_public.pem -pubin -in alice/session_key.txt -out alice/session_cipher.txt")

    with open("alice/session_cipher.txt", "r") as file:
        sign = file.read()
        file.close()

    sign = receiver + "\n" + tA + "\n" + sign

    print "sign: ", sign

    with open("alice/sign.txt", "w+") as file:
        file.write(sign)
        file.close()

    hashed = subprocess.check_output(("openssl", "dgst", "-sha256", "alice/sign.txt"))[-SHA256_LENGTH-1:]

    with open("alice/sign.txt", "w") as file:
        file.write(hashed)
        file.close()

    os.system("openssl rsautl -sign -in alice/sign.txt -inkey alice/private.pem -out alice/sig")


# with open("alice/session_cipher.txt", "r") as file:
#     session_cipher = file.read().strip()
#     file.close()

#with open("alice/sig", "r") as file:
#        session_cipher = session_cipher + file.read().strip()
#        file.close()


sign_session_key("Bob")