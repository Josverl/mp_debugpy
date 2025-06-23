import src._secrets as _secrets
import neopixel
from machine import Pin

np = neopixel.NeoPixel(Pin(15), 10)
np.fill((0, 0, 0))
np.write()

def do_connect():
    import machine, network
    wlan = network.WLAN()
    wlan.active(False)
    wlan.active(True)
    wlan.config(dhcp_hostname="debugee_esp32")
    if not wlan.isconnected():
        print(f'connecting to network... {_secrets.SSID}')
        wlan.connect(_secrets.SSID, _secrets.PASSWORD)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

do_connect()