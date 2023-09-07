import network
import time
import ubinascii

ssid = "Astra_Net" # here Your Router SSID
password = "astra2929" # your Router Password

# if you want to get Mac Address of your Pico

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("Mac Address: ", mac)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
