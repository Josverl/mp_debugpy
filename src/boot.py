import _secrets

def do_connect():
    import machine, network
    wlan = network.WLAN()
    wlan.active(False)
    wlan.active(True)
    wlan.config(dhcp_hostname="debugee_esp32")
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(_secrets.SSID, _secrets.PASSWORD)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

do_connect()