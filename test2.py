# all
import re
import time
import argparse
import I2C_driver as LCD
import smbus

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


bus = smbus.SMBus(1)
# IC address
address = 0x53
# x-axis, y-axis, z-axis adress
x_adr = 0x32
y_adr = 0x34
z_adr = 0x36


# ADXL345 init
def init_ADXL345():    
    print('ADXL345 init function')
    bus.write_byte_data(address, 0x2D, 0x08)

# data measure
def measure_acc(adr):    
    acc0 = bus.read_byte_data(address, adr)
    acc1 = bus.read_byte_data(address, adr + 1)
    acc = (acc1 << 8) + acc0
    if acc > 0x1FF:
        acc = (65536 - acc) * -1
    acc = acc * 3.9 / 1000
    return acc

def demo2(n, block_orientation, rotate, inreverse): #to show the input letter
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    with canvas(device) as draw:
        text(draw, (0, 0), look_dot, fill="white")

def demo(n, block_orientation, rotate, inreverse): #to show 1 2 3 4 5
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Created device")
    
#     for i in range(1,6):
#         i_str=str(i)
#         show_message(device, i_str, fill="white", font=proportional(CP437_FONT))
#         time.sleep(1)
        
    for i in range(1,6):
        i_str=str(i)
        with canvas(device) as draw:
            text(draw, (0, 0), i_str, fill="white")
            time.sleep(1)

#     # start demo
#     msg = "0123456789"
#     print(msg)
#     show_message(device, msg, fill="white", font=proportional(CP437_FONT))
#     time.sleep(1)
# 
#     show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0)
#     time.sleep(1)
# 
#     show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

#     #words= ['0','1','2','3','4','5','6','7','8','9']
#     words= ['O','X']
#     virtual = viewport(device, width=device.width, height=len(words) * 8)
#     with canvas(virtual) as draw:
#         for i, word in enumerate(words):
#             text(draw, (0, i * 8), word, fill="white", font=proportional(CP437_FONT))
#             time.sleep(0.1)
# 
#     for i in range(virtual.height - device.height):
#         virtual.set_position((0, i))
#         time.sleep(0.1)
# 
#     show_message(device, msg, fill="white")
# 
#     time.sleep(0.5)
# 
#     print('Canvas')
#     for i in words:
#         print(i, type(i))
#         with canvas(device) as draw:
#             #text(draw, (0, 0), "A", fill="white")
#             text(draw, (0, 0), i, fill="white")
#             
#         time.sleep(0.1)
#             
#         for _ in range(5):
#             for intensity in range(16):
#                 device.contrast(intensity * 16)
#                 time.sleep(0.5)
# 
#     device.contrast(0x80)
#     time.sleep(1)
# 
#     show_message(device, msg, fill="white", font=SINCLAIR_FONT)
# 
#     time.sleep(1)
#     show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
# 
#     time.sleep(1)
#     show_message(device, msg, fill="white", font=proportional(TINY_FONT))
# 
#     time.sleep(1)
#     show_message(device, msg)
# 
#     time.sleep(1)
#     for x in range(256):
#         with canvas(device) as draw:
#             text(draw, (0, 0), chr(x), fill="white")
#             time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        init_ADXL345()
        mylcd=LCD.lcd()
        while True:
            x_acc = measure_acc(x_adr)
            y_acc = measure_acc(y_adr)
            z_acc = measure_acc(z_adr)
            user=input('')
            if user=='1': 
                demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
            elif user=='2':
                mylcd.lcd_display_string("hi",1)
            elif user=='3':
                for i in range(1,4):
                    print ('X = %2.2f' % x_acc, '[g], Y = %2.2f' % y_acc, '[g], Z = %2.2f' % z_acc, '[g]')
                    time.sleep(1)
            elif user=='4':
                look_dot=input('')
                demo2(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
            elif user=='q':
                break
        mylcd.lcd_clear()
    except KeyboardInterrupt:
        pass

