try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import machine
import utime

button_Counter = 0

input_PinNo = 18
output_PinNo = 2  # You can define any GPIO pin here, like 3

button = machine.Pin(input_PinNo, machine.Pin.IN, machine.Pin.IN)  # Enable internal pull-up resistor
led = machine.Pin(output_PinNo, machine.Pin.OUT)

debounce_delay_ms = 1  # Adjust this value as needed (in milliseconds)

last_button_state = True  # Initialize the last button state
last_toggle_time = utime.ticks_ms()  # Initialize the last time the button was toggled

toggle_Flag = False

import gc
gc.collect()

ssid = 'iPhone' # replace with your Router SSID
password = 'net123456' #replace with your Router Password

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
led_state = "OFF"

def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
     <title>Pico W Webserver </title>
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border-radius: 15mm;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>Raspberry Pi Pico Web Server</h2>
    <p>LED state: <strong>""" + led_state + """</strong></p>
    <p>Button Pressed: <strong>""" + str(button_Counter) + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"led_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"led_off\"><button class="button button1">LED OFF</button></a>
    </p>
</body>

</html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
    current_time = utime.ticks_ms()
    button_value = button.value()
    
    # Check for a change in button state
    if button_value != last_button_state:
        last_button_state = button_value
        
        # Check if enough time has passed since the last toggle
        if utime.ticks_diff(current_time, last_toggle_time) >= debounce_delay_ms:
            toggle_Flag = not toggle_Flag
            led.value(toggle_Flag)
            last_toggle_time = current_time
            print("LED State Changed!")
            button_Counter = button_Counter+1
    try:


        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        led_on = request.find('/led_on')
        led_off = request.find('/led_off')
        if led_on == 6:
            print('LED ON -> GPIO25')
            led_state = "ON"
            led.on()
        if led_off == 6:
            print('LED OFF -> GPIO25')
            led_state = "OFF"
            led.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')