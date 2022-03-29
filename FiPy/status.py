import pycom
import machine
from machine import I2C
import time

#SLEEP_TIME = 1000*60*60*4
SLEEP_TIME = 1000*5
KG_TO_POUNDS = 2.205
commands = [0,1,2]
hiveStatus = [] # 4xN array of [id,weight,temp,humidity] lists

def writeData(dev,data):
    global hiveStatus
    it = next(dev)
    print("writing "+str(data)+ " to "+str(it))
    print(ord(data))
    hiveStatus[it].append(ord(data))
    print(ord(data))

# run this every interval
def run(scanBus, write, read):
    global hiveStatus
    hiveStatus=[]
    devs = devList(scanBus) # scan
    print("device list: ",end='')
    print(devs)
    for dev in devs:
        hiveStatus.append([dev])
    print('status list init: ',end='')
    print(hiveStatus)
    for i in range(3):
        print("command "+str(i))
        command(write, devs, commands[i]) # give pico sensor commands
        print("command done")
        time.sleep(1) # pause for sensor readings 
        print("paused")
        dev = iter(range(len(devs))) # create iter
        print("created iter")
        collect(read, devs, dev,# collect sensor data, save to hiveStatus
            writeData)# no lambdas in 3.4 :((
        print("collected data")
    pycom.rgbled(0x00AA00) # Green on success!
    return hiveStatus
    

# send command
def command(write, devs, cmd):
    for dev in devs:
        write(dev, bytes([cmd]))

# collect sensor readings
def collect(read, devs,devIt,dataRecip):
    for dev in devs:
        print("collecting for device "+str(dev))
        dataRecip(devIt,read(dev,1))

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