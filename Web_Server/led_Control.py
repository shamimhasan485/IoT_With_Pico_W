import network
import socket
import time
from machine import Pin

# Initialize the LED
led = Pin("LED", Pin.OUT)

# Define Wi-Fi credentials
ssid = 'Astra_Net'
password = 'astra2929'

# Initialize and connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# HTML template with a placeholder for status
html = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W</title>
</head>
<body>
    <h1>Pico W</h1>
    <p>%s</p>
</body>
</html>
"""

# Wait for Wi-Fi connection or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP Address:', status[0])

# Create a socket and bind it to 0.0.0.0 on port 80
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

# Listen for incoming connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print('led on =', led_on)
        print('led off =', led_off)

        if led_on == 6:
            print("LED ON")
            led.value(1)
            state = "LED is ON"
        elif led_off == 6:
            print("LED OFF")
            led.value(0)
            state = "LED is OFF"
        else:
            state = "Invalid command"

        response = html % state

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response.encode())  # Encode the response as bytes
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')
