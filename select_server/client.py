import socket
import hashlib
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('192.168.56.3', 8080))
message = input()
if not message : 
    s.close() 
    sys.exit(1)
message_in_bites = bytes(message, 'utf-8')
hash_object = hashlib.sha512(message_in_bites)
hash_dig = hash_object.digest()
s.sendall(hash_dig)
# data = s.recv(4096)
# print(data)
s.close() 

