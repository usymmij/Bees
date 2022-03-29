from network import Server
import pycom
import time
from network import WLAN
import machine
from network import LTE
from network import Bluetooth

pycom.heartbeat(False)

pycom.pybytes_on_boot(False) #we do not want Pybytes using the WLAN
pycom.smart_config_on_boot(False) #we also do not want smart config
pycom.wifi_on_boot(True)
pycom.wifi_mode_on_boot(WLAN.AP)
pycom.wifi_ssid_ap('bhive')
pycom.wifi_pwd_ap('')
pycom.rgbled(0x0A0A00)

server = Server(login=('b', 'ee'), timeout=300)

lte = LTE()
lte.deinit()
bluetooth = Bluetooth()
bluetooth.deinit()
machine.pygate_deinit()