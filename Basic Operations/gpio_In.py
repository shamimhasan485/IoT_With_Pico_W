import machine
import time

input_PinNo = 2

input_Pin = machine.Pin(input_PinNo, machine.Pin.IN)

while(True):
    pin_State = input_Pin.value()
    
    print("Input pin Value", pin_State)
    
    time.sleep(1)