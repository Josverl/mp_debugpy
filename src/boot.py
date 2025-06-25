import time

import _secrets

try:
    import neopixel
    from machine import Pin
    np = neopixel.NeoPixel(Pin(15), 10)
    np.fill((0, 0, 0))
    np.write()
except ImportError:
    np = None

def do_connect():
    import machine
    import network
    wlan = network.WLAN()
    wlan.active(False)
    wlan.active(True)
    try:
        wlan.config(dhcp_hostname="debugee_esp32")
    except Exception as e:
        print(f"Failed to set DHCP hostname: {e}")
    if not wlan.isconnected():
        wlan.connect(_secrets.SSID, _secrets.PASSWORD)
        start = time.ticks_ms()
        timeout = 10000  # 10 seconds in milliseconds
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                print("Failed to connect to WiFi: timeout")
                break
            machine.idle()
    print(f'network config: {wlan.config("dhcp_hostname")}.local {wlan.ipconfig("addr4")}')

do_connect()