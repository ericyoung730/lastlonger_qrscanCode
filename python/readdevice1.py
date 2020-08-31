from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
from demo_opts import get_device
from PIL import Image
import PIL.ImageOps

import wiringpi
import urllib
import audio
from threading import _Timer
import threading, time
import os
import socket

import fcntl
import struct
import os.path

class RepeatingTimer(_Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
import datetime
currentDT = datetime.datetime.now()

red_light_port=12
green_light_port=4
yellow_light_port=17
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(green_light_port, 1) # sets GPIO 24 to output
wiringpi.pinMode(red_light_port,1)
wiringpi.pinMode(yellow_light_port,1)
wiringpi.digitalWrite(green_light_port, 0)
wiringpi.digitalWrite(yellow_light_port,1)
wiringpi.digitalWrite(red_light_port,1)
global lock
lock=0


def check_network():
    global network_lock
    try:
        url="https://www.google.com"
        urllib.urlopen(url)
        print("reconnet")
        network_lock=0
    except:
        #print ("no connection")
        if(network_lock==0):
            currentDT = datetime.datetime.now()
            global fp
            fp = open("logger.txt", "a")
            fp.write("\n"+str(currentDT)+" wifi crashed")
            fp.close()
        network_lock=1

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, #SIOCGIFADDR
            struct.pack('256s',ifname[:15])
        )[20:24])
    except:
        return "nope"

    
print("Wifi: ", get_ip_address('wlan0'))
ssid = os.popen("iwconfig wlan0 \
                | grep 'ESSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'").read()
print("ssid: " + ssid)

fp = open("logger.txt", "a")
fp.write("\n"+str(currentDT)+"start logging")
fp.close()
device = get_device()
serial = spi(device=0, port=0)
device = ssd1309(serial)


status="Not connected"
try:
    url="https://www.google.com"
    urllib.urlopen(url)
    status="connected"
except:
    status="Not connected"

#print("hi")
with canvas(device) as draw:
    draw.text((10,20),ssid,fill="white")
    draw.text((10,30),get_ip_address('wlan0'),fill="white")
    draw.text((10,40),status,fill="white")

time.sleep(1)

if(status=="Not connected"):
    pos_zero=(0,0)
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images','status_noConnection.png'))
    logo = Image.open(img_path).convert('RGBA')
    for x in range(logo.width):
        for y in range(logo.height):
            a=logo.getpixel((x,y))
            if(a[3]==255):
                a=(255,255,255,255)
                logo.putpixel((x,y),a)
    background = Image.new("RGBA", device.size, "black")
    background.paste(logo,pos_zero)
    device.display(background.convert(device.mode))
    
    while(1):
        try:
            check_network()
            break
        except:
             print("no connection")
             time.sleep(10)
             
pos_zero=(0,0)
img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'status_idle.png'))
img_one = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_1.png'))
img_two = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_2.png'))
img_three = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_3.png'))
img_four = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_4.png'))
img_five = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_5.png'))
img_six = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_6.png'))
img_seven = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_7.png'))
img_eight = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_8.png'))
img_nine = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_9.png'))
img_zero = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_0.png'))
img_pound = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'id_digit_#.png'))
img_already = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'return_description_alreadyreturned.png'))
img_correct = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'return_description_succeed.png'))
img_error = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'return_description_error.png'))
img_sign = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'return_title_icon_error.png'))
img_check = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'return_title_icon_succeed.png'))
img_notGTG = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'error_notGTGcode.png'))
logo = Image.open(img_path).convert('RGBA')

background_idle = Image.new("RGBA", device.size, "black")
background_idle.paste(logo,pos_zero)

def readytoscan():
    global lock
    global network_lock
    if(lock==1):
        wiringpi.digitalWrite(yellow_light_port,1)
        wiringpi.digitalWrite(green_light_port,0)
        if network_lock==0:
            wiringpi.digitalWrite(red_light_port,1)
        else:
            wiringpi.digitalWrite(red_light_port,0)
        device.display(background_idle.convert(device.mode))
    else:
        lock=1
import sys
sys.path.append('/home/pi/.local/bin')
import evdev
import re
import API as api
Api=api.Api()
print(Api.apiKey)
global network_lock
network_lock=0
#apidata=Api.detailContainer("10652")
readyscan=RepeatingTimer(2.0, readytoscan)
readyscan.start()
checknet=RepeatingTimer(30.0, check_network)
checknet.start()
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
for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
            print (key_lookup)  # Print it all out!
            new+=key_lookup
            if key_lookup == 'CRLF':
                #lock=1
                currentDT = datetime.datetime.now()
                fp = open("logger.txt", "a")
                fp.write("\n"+str(currentDT)+":"+new)
                fp.close()
                
                Z=re.search('GOODTOGO',new)
                if Z is None:
                    pos_zero=(0,0)
                    logo = Image.open(img_notGTG).convert('RGBA')
                        #for x in range(logo.width):
                        #for y in range(logo.height):
                        #   a=logo.getpixel((x,y))
                        #   if(a[3]==255):
                        #       a=(255,255,255,255)
                        #       logo.putpixel((x,y),a)
                    background = Image.new("RGBA", device.size, "black")
                    background.paste(logo,pos_zero)
                    device.display(background.convert(device.mode))
                    lock=0
                        #with canvas(device) as draw:
                        #draw.rectangle(device.bounding_box, outline="white", fill="black")
                        #draw.text((10, 20), "error", fill="white")
                        # draw.text((10, 40), str(id), fill="white")
                    for n in audio.incorrect:
                        audio.play_note(n[0],n[1])
                    print ("none")
                    time.sleep(2)
                else:
                    m=re.search('\d+',new)
                    background = Image.new("RGBA", device.size, "black")
                    
                    print ("m.group(0):"+m.group(0))
                    print (len(m.group(0)))
                    print (m.group(0)[0])
                        #with canvas(device) as draw:
                        #draw.rectangle(device.bounding_box, outline="white", fill="black")
                        #draw.text((10, 20), "suceed", fill="white")
                        #draw.text((10, 40), m.group(0), fill="white")
                    for n in audio.correct:
                        audio.play_note(n[0],n[1])
                    try:
                        apidata=Api.returnContainer(m.group(0))
                        fp = open("logger.txt", "a")
                        fp.write(" wifi ok")
                        fp.close()
                        print('message :',apidata[1])
                        if(apidata[1]=='Already Return'):
                            wiringpi.digitalWrite(red_light_port,0)
                            wiringpi.digitalWrite(yellow_light_port,0)
                            logo = Image.open(img_check).convert('RGBA')
                            background.paste(logo,(8,6))
                            background.paste(logo,(104,6))
                            logo = Image.open(img_pound).convert('RGBA')
                            background.paste(logo,(34,6))
                            logo = Image.open(img_already).convert('RGBA')
                            background.paste(logo,(0,26))
                            for x in range(len(m.group(0)),0,-1):
                                print(m.group(0)[x-1])
                                if(m.group(0)[x-1]=='0'):
                                    logo = Image.open(img_zero).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='1'):
                                    logo = Image.open(img_one).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='2'):
                                    logo = Image.open(img_two).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='3'):
                                    logo = Image.open(img_three).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='4'):
                                    logo = Image.open(img_four).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='5'):
                                    logo = Image.open(img_five).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='6'):
                                    logo = Image.open(img_six).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='7'):
                                    logo = Image.open(img_seven).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='8'):
                                    logo = Image.open(img_eight).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='9'):
                                    logo = Image.open(img_nine).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                else:
                                    print("fuck yeah")
                            for y in range(5-len(m.group(0))):
                                logo = Image.open(img_zero).convert('RGBA')
                                background.paste(logo,(44+y*10,6))
                            device.display(background.convert(device.mode))
                            lock=0
                            time.sleep(2)
                        elif(apidata[1]=='Return Succeeded'):
                            wiringpi.digitalWrite(green_light_port,1)
                            wiringpi.digitalWrite(yellow_light_port,0)
                            wiringpi.digitalWrite(red_light_port,1)
                            logo = Image.open(img_check).convert('RGBA')
                            background.paste(logo,(8,6))
                            background.paste(logo,(104,6))
                            logo = Image.open(img_pound).convert('RGBA')
                            background.paste(logo,(34,6))
                            logo = Image.open(img_correct).convert('RGBA')
                            background.paste(logo,(0,26))
                            for x in range(len(m.group(0)),0,-1):
                                print(m.group(0)[x-1])
                                if(m.group(0)[x-1]=='0'):
                                    logo = Image.open(img_zero).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='1'):
                                    logo = Image.open(img_one).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='2'):
                                    logo = Image.open(img_two).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='3'):
                                    logo = Image.open(img_three).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='4'):
                                    logo = Image.open(img_four).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='5'):
                                    logo = Image.open(img_five).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='6'):
                                    logo = Image.open(img_six).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='7'):
                                    logo = Image.open(img_seven).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='8'):
                                    logo = Image.open(img_eight).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='9'):
                                    logo = Image.open(img_nine).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                else:
                                    print("fuck yeah")
                            for y in range(5-len(m.group(0))):
                                logo = Image.open(img_zero).convert('RGBA')
                                background.paste(logo,(44+y*10,6))
                            device.display(background.convert(device.mode))
                            lock=0
                            time.sleep(2)
                        else:
                            wiringpi.digitalWrite(red_light_port,0)
                            wiringpi.digitalWrite(yellow_light_port,0)
                            logo = Image.open(img_sign).convert('RGBA')
                            background.paste(logo,(8,6))
                            background.paste(logo,(104,6))
                            logo = Image.open(img_pound).convert('RGBA')
                            background.paste(logo,(34,6))
                            logo = Image.open(img_error).convert('RGBA')
                            background.paste(logo,(0,26))
                            for x in range(len(m.group(0)),0,-1):
                                print(m.group(0)[x-1])
                                if(m.group(0)[x-1]=='0'):
                                    logo = Image.open(img_zero).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='1'):
                                    logo = Image.open(img_one).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='2'):
                                    logo = Image.open(img_two).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='3'):
                                    logo = Image.open(img_three).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='4'):
                                    logo = Image.open(img_four).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='5'):
                                    logo = Image.open(img_five).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='6'):
                                    logo = Image.open(img_six).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='7'):
                                    logo = Image.open(img_seven).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='8'):
                                    logo = Image.open(img_eight).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                elif(m.group(0)[x-1]=='9'):
                                    logo = Image.open(img_nine).convert('RGBA')
                                    background.paste(logo,(84-(len(m.group(0))-x)*10,6))
                                else:
                                    print("fuck yeah")
                            for y in range(5-len(m.group(0))):
                                logo = Image.open(img_zero).convert('RGBA')
                                background.paste(logo,(44+y*10,6))
                            device.display(background.convert(device.mode))
                            lock=0
                            time.sleep(2)
                    except:
                        fp = open("logger.txt", "a")
                        fp.write(" wifi not ok")
                        fp.close()
                        print("no network")
                    #print(list(apidata))
                    time.sleep(2)
                new= " "
