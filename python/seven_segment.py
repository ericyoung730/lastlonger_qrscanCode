import wiringpi
import time
wiringpi.wiringPiSetupGpio()
segments = (27,22,5,6,26,20,21)
digitZero= (1,1,1,1,1,1,0)
digitOne=  (0,1,1,0,0,0,0)
digitTwo=  (1,1,0,1,1,0,1)
digitEight=(1,1,1,1,1,1,1)
digitNine=(1,1,1,1,0,1,1)
for segment in segments:
    wiringpi.pinMode(segment, 1)
    wiringpi.digitalWrite(segment, 0)
try:
    while True:
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop], digitZero[loop])
        time.sleep(1)
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop], digitOne[loop])
        time.sleep(1)
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop],digitTwo[loop])
        time.sleep(1)
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop],digitEight[loop])
        time.sleep(1)
        for loop in range (0,7):
            wiringpi.digitalWrite(segments[loop],digitNine[loop])
        time.sleep(1)

except KeyboardInterrupt:

    print("bye")
