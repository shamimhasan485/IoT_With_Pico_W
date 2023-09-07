import machine
import time

led = machine.Pin("LED", machine.Pin.OUT) #define the led pin as output


while(True):
    #You can use this to toggle the led state
    led.toggle()
    time.sleep(1)
    
    #Or You can use this to turn on and off after certain time
    
    #led.off()
    #time.sleep(1)
    #led.on()
    #time.sleep(1)