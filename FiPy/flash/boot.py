from network import Server
import pycom
import time
from network import WLAN
from machine import Pin
exitPin = Pin('P23', mode = Pin.IN)

if exitPin() == 1:
    pycom.pybytes_on_boot(False) #we do not want Pybytes using the WLAN
    pycom.smart_config_on_boot(False) #we also do not want smart config
    pycom.wifi_on_boot(True)
    pycom.wifi_mode_on_boot(WLAN.AP)
    pycom.wifi_ssid_ap('bhive')
    pycom.wifi_pwd_ap('')


server = Server(login=('b', 'ee'), timeout=300)

pycom.heartbeat(False)
pycom.rgbled(0xA0A000)