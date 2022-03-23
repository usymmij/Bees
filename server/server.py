import socket
import time
import csv
import datetime 
import os.path

HOST = "127.0.0.1" 
PORT = 6500

def tcpserver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(2048)
                    if not data:
                        break
                    hives,err = process(data)
                    if(err):
                        conn.sendall(b'F')
                        continue
                    conn.sendall(b'T')
                    save(hives)
                    break
            #time.sleep(60*60*7)
            time.sleep(5)

def process(data):
    data = data.decode('utf-8')
    i = 0
    hives = []
    try:
        if True:
            if data[0] == '\n':
                next=True
                i+=1
                while(next):
                    hive = []
                    for b in range(4):
                        hive.append(ord(data[i]))
                        i+=1

                    print(f'received {hive}')
                    print("hive: "+str(hive[0]))
                    hives.append(hive)
                    if i == len(data):
                        next=False
                        continue
                    if data[i]=='\n':
                        i+=1
                        continue
            return hives,False
    except:
        print("faulty packet received")
        return [], True

def save(hives):
    now = datetime.datetime.now()
    for hive in hives:
        formatted = [int(time.time()), (hive[1]),(hive[2]),(hive[3])]
        save_loc = './data/'
        save_loc += str(now.year)+"."+str(hive[0])+".csv"
        print(save_loc)
        if False == os.path.exists(save_loc):
            f = open(save_loc, "w")
            f.close()
        with open(save_loc, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(formatted)
    

    
if __name__ == "__main__":
    tcpserver();