import pycom
import machine
from machine import I2C
import time

#SLEEP_TIME = 1000*60*60*4
SLEEP_TIME = 1000*5
KG_TO_POUNDS = 2.205
commands = [0,1,2]
hiveStatus = [] # 4xN array of [id,weight,temp,humidity] lists

def writeData():
    hiveStatus[next(dev)].append(int.frombytes(data,'little'))

# run this every interval
def run(scanBus, write, read):
    devs = devList(scanBus) # scan
    for dev in devs:
        hiveStatus.append([dev])
    for i in range(3):
        command(write, devs, commands[i]) # give pico sensor commands
        time.sleep(1) # pause for sensor readings 
        dev = iter(range(len(devs))) # create iter
        collect(read, devs, # collect sensor data, save to hiveStatus
            writeData)# no lambdas in 3.4 :((
    pycom.rgbled(0x00AA00) # Green on success!
    return hiveStatus
    

# send command
def command(write, devs, cmd):
    for dev in devs:
        packet = []
        for ch in cmd:
            packet.append(ord(ch))
        write(dev, bytes(packet))

# collect sensor readings
def collect(read, devs, dataRecip):
    for dev in devs:
        dataRecip(read(dev,4))

# scan devices
def devList(scan):
    scanning = True
    dList = []
    while scanning:
        try:
            dList = scan()
            scanning = False
        except:
            machine.sleep()
            continue
    return dList

# convert kgs to lbs
def toPounds(kgs):
    return kgs*KG_TO_POUNDS

if __name__ == "__main__":
    pycom.rgbled(0xA0A000) # yellow on boot
    i2c = I2C(2, I2C.MASTER, baudrate=10000)
    status = run(i2c.scan,i2c.writeto, i2c.readfrom)