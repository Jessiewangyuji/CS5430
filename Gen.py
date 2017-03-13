import os

os.system('openssl genrsa -des3 -out alice/private.pem 2048')
os.system('openssl rsa -in alice/private.pem -outform PEM -pubout -out alice/a_public.pem')
os.system('openssl genrsa -des3 -out bob/private.pem 2048')
os.system('openssl rsa -in bob/private.pem -outform PEM -pubout -out bob/b_public.pem')
os.system('cp alice/a_public.pem bob/a_public.pem')
os.system('cp bob/b_public.pem alice/b_public.pem')
os.system('cp alice/a_public.pem mallory/a_public.pem')
os.system('cp bob/b_public.pem mallory/b_public.pem')

