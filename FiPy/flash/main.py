from pickle import TRUE
import status
import pycom
from machine import Pin
from machine import I2C

SLEEP_TIME = 1000*5
exitPin = Pin('P23', mode = Pin.IN)

def main():
    if exitPin() == 1:
        return
    pycom.rgbled(0xA0A000) # yellow on boot
    i2c = I2C(2, I2C.MASTER, baudrate=10000)

    pycom.rgbled(0x010002) # pink on data collection
    status.run(i2c.scan,i2c.writeto, i2c.readfrom)

    pycom.rgbled(0x0000A0) # blue on communication
    

    machine.deepsleep(SLEEP_TIME) # wait for next read cycle



if __name__ == "__main__":
    main()
