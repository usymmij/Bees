import socket
import random
import time

print(int(time.time()))
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6500  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = ''
    for hive in range(15):
        hiveDat = '\n'
        hiveDat += chr(hive)
        hiveDat += chr(random.randint(0,255))#weight
        hiveDat += chr(random.randint(0,255))#temp
        hiveDat += chr(random.randint(0,255))#humidity
        data += hiveDat
    ret = b'F'
    while(ret==b'F'):
        s.sendall(data.encode('utf-8'))
        ret = s.recv(1)
        break
ret=ret.decode('utf-8')
print(f"Received {ret}")