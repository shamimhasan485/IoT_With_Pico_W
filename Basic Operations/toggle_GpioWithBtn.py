import machine
import time

input_PinNo = 2
output_PinNo = "LED" # you can define here any gpio pin like 3


button = machine.Pin(input_PinNo, machine.Pin.IN)
led = machine.Pin(output_PinNo, machine.Pin.OUT)

toggle_Flag = False

while (True):
    button_Value = button.value()
    print("Button Value", button_Value)
    
    if button_Value:
        toggle_Flag = not toggle_Flag
        led.value(toggle_Flag)
        time.sleep(1)
    time.sleep(.050)