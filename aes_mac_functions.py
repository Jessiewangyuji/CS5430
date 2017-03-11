import socket
import time
import os
import sys
import subprocess


def enc(message,key,iv):
	echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
	openssl_output = subprocess.check_output(("openssl", "enc", "-aes-256-cbc", "-base64", "-K", key, "-iv", iv), stdin=echo_program.stdout).strip()
	return openssl_output

def mac(message,key):
	echo_program = subprocess.Popen(('echo', message), stdout=subprocess.PIPE)
	openssl_output = subprocess.check_output(("openssl", "sha256", "-hmac", key), stdin=echo_program.stdout)[9:].strip()
	return openssl_output

def enc_mac(message,enc_key,mac_key,iv):
	encrypted_message = enc(message,enc_key,iv)
	tag = mac(iv + encrypted_message,mac_key)
	return encrypted_message,tag


def dec(message,key,iv):
	echo_program = subprocess.Popen(('echo',message), stdout=subprocess.PIPE)
	openssl_output = subprocess.check_output(("openssl", "enc", "-d", "-aes-256-cbc", "-base64", "-K", key, "-iv", iv), stdin=echo_program.stdout).strip()
	return openssl_output


def verify_mac(message,key,tag):
	return tag == mac(message,key)




message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
key = '12345'
iv = '98f093'

encrypted = enc(message,key,iv)
print(encrypted)
decrypted = dec(encrypted,key,iv)
print(decrypted)

tag = mac(message,key)
print(verify_mac(message,key,tag))



# echo_program = subprocess.Popen(('echo', message), stdout=subprocess.PIPE)
# openssl_output = subprocess.check_output(("openssl", "sha256", "-hmac", key), stdin=echo_program.stdout)[9:].strip()
# echo_program.stdout.close()
# sed_output = subprocess.check_output(("sed", "s/^.* //"), stdin=openssl_program.stdout).strip()
# print(openssl_output)



