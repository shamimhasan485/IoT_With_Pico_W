import machine
import time

output_PinNo = 3

output_Pin = machine.Pin(output_PinNo, machine.Pin.OUT)

while(True):
    output_Pin.on()
    print("Output Pin is on!")
    time.sleep(1)
    
    output_Pin.off()
    print("Output Pin is off!")
    time.sleep(1)