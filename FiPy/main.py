import status
import upload
import pycom
from machine import I2C
import machine as m
import time

SLEEP_TIME = 1000*5
hiveStatus= None

def main():
    global hiveStatus
    pycom.rgbled(0xA0A0A0) # yellow on boot
    i2c = I2C(0, I2C.MASTER, baudrate=2000)

    pycom.rgbled(0x0A000A) # pink on data collection
    try:
        hiveStatus=status.run(i2c.scan,i2c.writeto, i2c.readfrom)
    except:
        pycom.rgbled(0x0A0A0A) # white failure

    pycom.rgbled(0x00000A) # blue on communication
    try:
        upload.send(hiveStatus)
    except:
        pycom.rgbled(0x0A0A0A) # white failure

    #client = upload.uploadClient()
    #client.setup()
    #client.sendData(hiveStatus)
    #m.deepsleep(SLEEP_TIME) # wait for next read cycle

def tryStatus():
    pycom.rgbled(0xA0A0A0) # yellow on boot
    i2c = I2C(0, I2C.MASTER, baudrate=2000)

    pycom.rgbled(0x0A000A) # pink on data collection
    try:
        print(status.run(i2c.scan,i2c.writeto, i2c.readfrom))
        pycom.rgbled(0x00AA00) # pink on data collection
    except:
        pycom.rgbled(0xAA0000)
    i2c.deinit()

def getIds():
    hi=1
    return [0,2,4,6,8]
def printAddMess(add,mess):
    print('address:'+str(add)+', command:'+str(mess))
def printAdd(add,length):
    print('read from'+str(add))
    return 5
def testStatus():
    global hiveStatus
    pycom.rgbled(0x0A0000)
    time.sleep(1)
    hiveStatus = status.run(getIds,printAddMess,printAdd)
    print("status:")
    print(hiveStatus)

if __name__ == "__main__":
    #main(hiveStatus)
    #testStatus()
    pass
