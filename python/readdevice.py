from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
import audio
import threading, time
serial = spi(device=0, port=0)
device = ssd1309(serial)
def readytoscan():
    timer=threading.Timer(5,readytoscan)
    timer.start()
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 20), "welcome to goodTogo", fill="white")

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
readytoscan()
# substitute ssd1331(...) or sh1106(...) below if using that device
import sys
sys.path.append('/home/pi/.local/bin')
import evdev
import re
import API as api
Api=api.Api()
print(Api.apiKey)
from evdev import InputDevice, categorize, ecodes
new = ""
dev = InputDevice("/dev/input/event0") # my keyboard
# Provided as an example taken from my own keyboard attached to a Centos 6 box:
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 20), "welcome to goodTogo", fill="white")
for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
            # print (key_lookup)  # Print it all out!
            new+=key_lookup
            if key_lookup == 'CRLF':
                lock=1
                Z=re.search('GOODTOGO',new)
                if Z is None:
                    
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((10, 20), "error", fill="white")
                       # draw.text((10, 40), str(id), fill="white")
                    
                    for n in audio.incorrect:
                        audio.play_note(n[0],n[1])
                    print ("none")
                    time.sleep(2)
                else:
                    m=re.search('\d+',new)
                    print (m.group(0))
                    
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((10, 20), "suceed", fill="white")
                        draw.text((10, 40), m.group(0), fill="white")
                    
                    for n in audio.correct:
                        audio.play_note(n[0],n[1])
                    apidata=Api.returnContainer(m.group(0))
                    print(list(apidata))
                    time.sleep(2)
                new= " "
