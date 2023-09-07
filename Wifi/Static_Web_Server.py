import network
import socket
import time
from machine import Pin

# Define Wi-Fi credentials
ssid = 'Astra_Net' # Replace With Your Router SSID
password = 'astra2929' # Replace with your Router Password

# Initialize the LED
led = Pin("LED", Pin.OUT)

# Initialize and connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# HTML response to be served
html = """<!DOCTYPE html>
<html>
<head>
<style>
body {background-color: powderblue;}
h1   {color: blue;}
p    {color: red;}
</style>
</head>
<body>

<h1>Hello From Pico W</h1>
<p>This is a paragraph.</p>

</body>
</html>
"""

# Wait for Wi-Fi connection or timeout
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
    print("Goto Your browser and hit the ip[must be connected in the same network]")

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
        cl_file = cl.makefile('rwb', 0)

        # Read and discard HTTP request headers
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        # Send the HTML response
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')
