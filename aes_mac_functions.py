import subprocess
import os
import pickle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF 
from cryptography.hazmat.backends import default_backend

HMAC_TAG_LENGTH = 64
IV_LENGTH = 32

DEVNULL = open(os.devnull,'w')

def enc(message,key,iv):
    echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
    encrypted_message = subprocess.check_output(("openssl", "enc", "-aes-256-cbc", "-base64", "-K", key, "-iv", iv), stdin=echo_program.stdout).strip()
    return encrypted_message

def mac(message,key):
    echo_program = subprocess.Popen(('echo', message), stdout=subprocess.PIPE)
    tag = subprocess.check_output(("openssl", "dgst", "-sha256", "-hmac", key), stdin=echo_program.stdout)[-HMAC_TAG_LENGTH-1:].strip()
    return tag

def enc_mac(message,enc_key,mac_key,iv):
    encrypted_message = enc(message,enc_key,iv)
    final_message = pickle.dumps([iv,encrypted_message])
    tag = mac(final_message,mac_key)
    return tag,final_message


def dec(message,key,iv):
    echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
    decrypted_message = subprocess.check_output(("openssl", "enc", "-d", "-aes-256-cbc", "-base64", "-K", key, "-iv", iv), stdin=echo_program.stdout, stderr = DEVNULL).strip()
    return decrypted_message


def verify_mac(message,key,tag):
    return tag == mac(message,key)



def derive_key(session_key,salt):

    backend = default_backend()

    hkdf = HKDF(
        algorithm = hashes.SHA256(),
        length = 64,
        salt = salt,
        info = None,
        backend = backend
        )

    return hkdf.derive(session_key)





# message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'

# key = '12345'

# print(mac(message,key))

# iv = '19584938493829384728382938482732'

# tag,encrypted = enc_mac(message,key,key,iv)
# raw_message = tag + encrypted
# tag,message = get_tag_and_message(raw_message)
# print(verify_mac(message,key,tag))
# iv,message = get_iv_and_message(message)
# print(dec(message,key,iv))


# iv,message = get_iv_and_message(message)
# print(dec(message,key,iv))


# echo_program = subprocess.Popen(('echo', message), stdout=subprocess.PIPE)
# openssl_output = subprocess.check_output(("openssl", "sha256", "-hmac", key), stdin=echo_program.stdout)[9:].strip()
# echo_program.stdout.close()
# sed_output = subprocess.check_output(("sed", "s/^.* //"), stdin=openssl_program.stdout).strip()
# print(openssl_output)



