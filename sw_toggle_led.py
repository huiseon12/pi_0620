#switch and led
import RPi.GPIO as GPIO  #Import Raspberry Pi GPIO library
import I2C_driver as LCD
import time

GPIO.setwarnings(False)  #Ignore warning for now
GPIO.setmode(GPIO.BOARD)  #Use physical pin numbering

LED=16
Switch=10

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
#Set pin 15 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(Switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mylcd= LCD.lcd()

switch = 0
pre_switch = 0

try:
    while True:
        if GPIO.input(Switch) == GPIO.HIGH: 
            time.sleep(0.2)
            switch=~switch
        
        if pre_switch!=switch:
            mylcd.lcd_clear()
            if switch==0: #led on
                mylcd.lcd_display_string("LED ON",1)
                GPIO.output(LED, GPIO.HIGH)
        
            else:
                GPIO.output(LED, GPIO.LOW) #led off
                mylcd.lcd_display_string("LED OFF",1)
        
        pre_switch=switch
        
except KeyboardInterrupt:
    mylcd.lcd_clear()