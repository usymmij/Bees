import status
import upload
import pycom
from machine import Pin
from machine import I2C
import time

SLEEP_TIME = 1000*5
exitPin = Pin('P23', mode = Pin.IN)
hi = 0

def main():
    if exitPin() == 0:
        pycom.rgbled(0x0A0000) # red if exit
        return
    pycom.rgbled(0xA0A000) # yellow on boot
    i2c = I2C(2, I2C.MASTER, baudrate=10000)

    pycom.rgbled(0x0A000A) # pink on data collection
    hiveStatus = status.run(i2c.scan,i2c.writeto, i2c.readfrom)

    pycom.rgbled(0x00000A) # blue on communication
    client = upload.uploadClient()
    client.setup()
    client.sendData(hiveStatus)
    #machine.deepsleep(SLEEP_TIME) # wait for next read cycle

def getIds():return[0,2,4,6,8];
def printAddMess(add,mess):print(f'address:{add}, command:{mess}')
def printAdd(add):print(f'read from{add}')
def testStatus():
    pycom.rgbled(0x0A0000)
    time.sleep(1)
    hiveStatus = status.run(getIds,printAddMess,printAdd)

if __name__ == "__main__":
    #main()
    testStatus()
    pass
