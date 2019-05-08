import serial
import time
import re
ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

import API as api
Api=api.Api()
print(Api.apiKey)
while True:

	read_ser=ser.readline()
	m=re.search('\d+',read_ser)
	print(m.group(0))
	print(read_ser)
    print(Api.returnContainer(m.group(0)))
