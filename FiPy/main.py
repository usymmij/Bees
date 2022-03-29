import status
import upload
import pycom
from machine import I2C
from machine import Pin
import machine as m
import time

SLEEP_TIME = 1000*60*1
hiveStatus= None
p8 = Pin('P8', mode=Pin.OUT)
p8.value(1)
m.sleep(3000,True)

def main():
    global hiveStatus
    i2c = I2C(0, I2C.MASTER, baudrate=2000)

    pycom.rgbled(0x0A000A) # pink on data collection
    try:
        hiveStatus=status.run(i2c.scan,i2c.writeto, i2c.readfrom)
    except:
        pycom.rgbled(0x0A0A0A) # white failure
        return

    p8.value(0)
    pycom.rgbled(0x00000A) # blue on communication
    try:
        upload.send(hiveStatus)
    except:
        pycom.rgbled(0x0A0A0A) # white failure
        return

    #client = upload.uploadClient()
    #client.setup()
    #client.sendData(hiveStatus)
    p8.hold(True)
    time.sleep_ms(SLEEP_TIME)
    #m.deepsleep(SLEEP_TIME) # wait for next read cycle

def tryStatus():
    pycom.rgbled(0xA0A0A0) # yellow on boot
    i2c = I2C(0, I2C.MASTER, baudrate=2000)

    pycom.rgbled(0x0A000A) # pink on data collection
    try:
        print(status.run(i2c.scan,i2c.writeto, i2c.readfrom))
        pycom.rgbled(0x00AA00) # green on success
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

def testUpload():
    upload.send([[8,1,2,3]])

if __name__ == "__main__":
    main()
    #testStatus()
    pass
