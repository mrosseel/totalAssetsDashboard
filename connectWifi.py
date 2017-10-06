# improve using http://docs.micropython.org/en/v1.9.1/wipy/wipy/tutorial/wlan.html

def connect(ssid, password):
    import network

    station = network.WLAN(network.STA_IF)

    if station.isconnected() == True:
        print("Already connected")
        print(station.ifconfig())
        return

    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    print("Connection successful")
    print(station.ifconfig())
