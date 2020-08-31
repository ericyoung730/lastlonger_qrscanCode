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

segments = (27,22,5,6,26,20,21)
digitZero= (1,1,1,1,1,1,0)
digitOne=  (0,1,1,0,0,0,0)
digitTwo=  (1,1,0,1,1,0,1)
digitEight=(1,1,1,1,1,1,1)
digitNine=(1,1,1,1,0,1,1)
for segment in segments:
    wiringpi.pinMode(segment, 1)
    wiringpi.digitalWrite(segment, 0)
    
red_light_port=12
white_light_port=4
green_light_port=17

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(green_light_port, 1) # sets GPIO 24 to output
wiringpi.pinMode(red_light_port,1)
wiringpi.pinMode(white_light_port,1)

global lock
lock=0

import subprocess
while True:
    try:
        ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        print (output)
        if output[29:32]=='off':
            print('no wifi')
            i=1/0
        break
    except:
      # grep did not match any lines
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop], digitEight[loop])
while True:
    try:
        url="https://www.google.com"
        urllib.urlopen(url)
        print ("network ok")
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop],0)
        wiringpi.digitalWrite(white_light_port,1)
        break
    except:
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop], digitNine[loop])
        wiringpi.digitalWrite(white_light_port,0)
        time.sleep(1)
def check_network():
    global network_lock
    if network_lock==1:
        try:
            url="https://www.google.com"
            urllib.urlopen(url)
            print("reconnet")
            network_lock=0
            for loop in range (0,7):
                wiringpi.digitalWrite(segments[loop],0)
            wiringpi.digitalWrite(white_light_port,1)
        except:
            #print ("no connection")
            for loop in range (0,7):
                wiringpi.digitalWrite(segments[loop], digitNine[loop])
            wiringpi.digitalWrite(white_light_port,0)
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

status="Not connected"
try:
    url="https://www.google.com"
    urllib.urlopen(url)
    status="connected"
except:
    status="Not connected"

if(status=="Not connected"):
    while(1):
        try:
            check_network()
            break
        except:
             print("no connection")
             time.sleep(10)
def readytoscan():
    global lock
    global network_lock
    if(lock==1):
        wiringpi.digitalWrite(white_light_port,1)
       # wiringpi.digitalWrite(green_light_port,0)
        #if network_lock==0:
           # wiringpi.digitalWrite(red_light_port,1)
        #else:
           # wiringpi.digitalWrite(red_light_port,0)
    else:
        lock=1
import sys
sys.path.append('/home/pi/.local/bin')
import evdev
import re
import API as api
Api=api.Api()
print(Api.apiKey)
wiringpi.digitalWrite(green_light_port, 0)
wiringpi.digitalWrite(white_light_port,1)
wiringpi.digitalWrite(red_light_port,1)
global network_lock
network_lock=1
#apidata=Api.detailContainer("10652")
#readyscan=RepeatingTimer(2.0, readytoscan)
#readyscan.start()
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
                wiringpi.digitalWrite(white_light_port,0)
                currentDT = datetime.datetime.now()
                fp = open("logger.txt", "a")
                fp.write("\n"+str(currentDT)+":"+new)
                fp.close()
                
                Z=re.search('GOODTOGO',new)
                print (len(new))
                #Z=re.search('C/',new)
                if len(new)<15:
                    lock=0
                    for n in audio.incorrect:
                        audio.play_note(n[0],n[1])
                    wiringpi.digitalWrite(green_light_port, 0)
                    wiringpi.digitalWrite(white_light_port,0)
                    for loop in range (0,7):
                        wiringpi.digitalWrite(segments[loop], digitOne[loop])
                    time.sleep(3)
                    for loop in range (0,7):
                        wiringpi.digitalWrite(segments[loop],0)
                        lock=0
                    wiringpi.digitalWrite(green_light_port,0)
                    wiringpi.digitalWrite(white_light_port,1)
                    print ("scan too fast")
                    time.sleep(2)
                elif Z is None:
                    lock=0
                    for n in audio.incorrect:
                        audio.play_note(n[0],n[1])
                    wiringpi.digitalWrite(green_light_port, 0)
                    wiringpi.digitalWrite(white_light_port,0)
                    for loop in range (0,7):
                        wiringpi.digitalWrite(segments[loop], digitTwo[loop])
                    time.sleep(3)
                    for loop in range (0,7):
                        wiringpi.digitalWrite(segments[loop],0)
                        lock=0
                    wiringpi.digitalWrite(green_light_port,0)
                    wiringpi.digitalWrite(white_light_port,1)
                    print ("none")
                    time.sleep(2)
                else:
                    wiringpi.digitalWrite(white_light_port,0)
                    wiringpi.digitalWrite(green_light_port,1)
                    for n in audio.correct:
                        audio.play_note(n[0],n[1])
                    m=re.search('\d+',new)
                    print ("m.group(0):"+m.group(0))
                    print (len(m.group(0)))
                    print (m.group(0)[0])
                    
                    try:
                        
                        apidata=Api.returnContainer(m.group(0),32)
                        fp = open("logger.txt", "a")
                        fp.write(" wifi ok")
                        fp.close()
                        
                        print(apidata[0])
                        print('message :',apidata[1])
                        if(apidata[1]=='Already Return'):
                            print(" i am already")
                            #for n in audio.correct:
                             #   audio.play_note(n[0],n[1])
                            
                            wiringpi.digitalWrite(green_light_port,1)
                            lock=0
                            #time.sleep(3)
                            wiringpi.digitalWrite(green_light_port,0)
                            wiringpi.digitalWrite(white_light_port,1)
                        elif(apidata[0]==200):
                            print("i am 200 ok'")
                            #for n in audio.correct:
                             #   audio.play_note(n[0],n[1])
                            wiringpi.digitalWrite(green_light_port,1)
                            lock=0
                            #time.sleep(3)
                            wiringpi.digitalWrite(green_light_port,0)
                            wiringpi.digitalWrite(white_light_port,1)
                        elif(apidata[1]=='Return Succeeded'):
                            print(" i am sucess")
                            #for n in audio.correct:
                             #   audio.play_note(n[0],n[1])
                            wiringpi.digitalWrite(green_light_port,1)
                            lock=0
                            #time.sleep(3)
                            wiringpi.digitalWrite(green_light_port, 0)
                            wiringpi.digitalWrite(white_light_port,1)
                        else:
                            print("i am error")
                            #for n in audio.incorrect:
                             #   audio.play_note(n[0],n[1])
                            #for n in audio.correct:
                             #   audio.play_note(n[0],n[1])
                            #for loop in range (0,7):
                              #  wiringpi.digitalWrite(segments[loop],digitOne[loop])
                            lock=0
                            #time.sleep(3)
                           # for loop in range (0,7):
                            #    wiringpi.digitalWrite(segments[loop],0)
                            wiringpi.digitalWrite(green_light_port, 0)
                            wiringpi.digitalWrite(white_light_port,1)
                    except:
                        network_lock=1
                        fp = open("logger.txt", "a")
                        fp.write(" wifi not ok")
                        fp.close()
                        for loop in range (0,7):
                            wiringpi.digitalWrite(segments[loop], digitNine[loop])
                        print("no network")
                    #print(list(apidata))
                    time.sleep(2)
                new= " "
