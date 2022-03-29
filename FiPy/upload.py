import pycom
import machine
import time
import socket
from network import WLAN
HOST = "192.168.4.2"  # The server's hostname or IP address
PORT = 6500  # The port used by the server

def send(data):
    message = ''
    for i in range(len(data)):
        hiveDat='\n'
        hiveDat += chr(data[i][0])
        hiveDat += chr(data[i][1])
        hiveDat += chr(data[i][2])
        hiveDat += chr(data[i][3])
        message += hiveDat
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except OSError as e:
        pass
    ret = b'F'
    while(ret==b'F'):
        s.sendall(message.encode('utf-8'))
        ret = s.recv(1)

# not doing lte stuff for now, since server is unable to be port forwarded
#class uploadClient:
#    def send(self,data):
#        try:
#            self.lte = LTE()
#            self.lte.attach(band=20, apn="iot.truphone.com")
#            print("attaching..",end='')
#            while not self.lte.isattached():
#                time.sleep(0.25)
#                print('.',end='')
#            print('attached!')
#
#            self.lte.connect()
#            print("connecting..",end='')
#            while not self.lte.isconnected():
#                time.sleep(0.25)
#                print('.',end='')
#            print("connected!")
#            return True
#        except:
#            return False
#
#    def disconnect(self):
#        try:
#            self.lte.deinit()
#            return True
#        except:
#            return False
#    
#    def sendData(self, data):
#        HOST = "127.0.0.1"  # The server's hostname or IP address
#        #HOST= ""
#        PORT = 6500  # The port used by the server
#        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#            s.connect((HOST, PORT))
#            ret = b'F'
#            while(ret==b'F'):
#                s.sendall(data.encode('utf-8'))
#                ret = s.recv(1)

if __name__ == "__main__":
    pass