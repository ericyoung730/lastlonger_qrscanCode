import wiringpi
import time, sys

PIN = 18
BEAT = 0.05

DELAY = 0.1

# NOTE TYPES

# NOTE			FREQUENCY
B7			=	int(3951.07)
A7_SHARP	=	int(3729.31)
A7			=	int(3620.00)
G7_SHARP	=	int(3322.44)
G7			=	int(3135.96)
F7_SHARP	=	int(2959.96)
F7			=	int(2793.83)
E7			=	int(2637.02)
D7_SHARP	=	int(2489.02)
D7			=	int(2349.32)
C7_SHARP	=	int(2217.46)
C7			=	int(2093.00) # DOUBLE HIGH C
B6			=	int(1975.53)
A6_SHARP	=	int(1864.66)
A6			=	int(1760.00)
G6_SHARP	=	int(1661.22)
G6			=	int(1567.98)
F6_SHARP	=	int(1479.98)
F6			=	int(1396.91)
E6			=	int(1318.51)
D6_SHARP	=	int(1244.51)
D6			=	int(1174.66)
C6_SHARP	=	int(1108.73)
C6			=	int(1046.51) # HIGH C
B5			=	int(987.767)
A5_SHARP	=	int(932.328)
A5			=	int(880.000)
G5_SHARP	=	int(830.609)
G5			=	int(783.991)
F5_SHARP	=	int(739.989)
F5			=	int(698.456)
E5			=	int(659.255)
D5_SHARP	=	int(622.254)
D5			=	int(587.330)
C5_SHARP	=	int(554.365)
C5			=	int(523.251) # TENOR C
B4			=	int(493.883)
A4_SHARP	=	int(466.164)
A4			=	int(440.000)
G4_SHARP	=	int(415.305)
G4			=	int(391.995)
F4_SHARP	=	int(369.994)
F4			=	int(349.228)
E4			=	int(329.628)
D4_SHARP	=	int(311.127)
D4			=	int(293.665)
C4_SHARP	=	int(277.183)
C4			=	int(261.626) # MIDDLE C
B3			=	int(246.942)
A3_SHARP	=	int(233.082)
A3			=	int(220.000)
G3_SHARP	=	int(207.652)
G3			=	int(195.998)
F3_SHARP	=	int(184.997)
F3			=	int(174.614)
E3			=	int(164.814)
D3_SHARP	=	int(155.563)
D3			=	int(146.832)
C3_SHARP	=	int(138.591)
C3			=	int(130.813) # LOW C
B2			=	int(123.471)
A2_SHARP	=	int(116.541)
A2			=	int(110.000)
G2_SHARP	=	int(103.826)
G2			=	int(97.9989)
F2_SHARP	=	int(92.4986)
F2			=	int(87.3071)
E2			=	int(82.4069)
D2_SHARP	=	int(77.7817)
D2			=	int(73.4162)
C2_SHARP	=	int(69.2957)
C2			=	int(65.4064) # DEEP C
B1			=	int(61.7354)
A1_SHARP	=	int(58.2705)
A1			=	int(55.0000)
G1_SHARP	=	int(51.9131)
G1			=	int(48.9994)
F1_SHARP	=	int(46.2493)
F1			=	int(43.6535)
E1			=	int(41.2034)
D1_SHARP	=	int(38.8909)
D1			=	int(36.7081)
C1_SHARP	=	int(34.6478)
C1			=	int(32.7032)
B0			=	int(30.8677)
A0_SHARP	=	int(29.1352)
A0			=	int(27.5000)

music = [(C4, BEAT), (C4, BEAT), (C4, BEAT), (0, (BEAT/2)), (C4, BEAT), (B3, BEAT), (A3, BEAT), (B3, BEAT), (C4, BEAT), (D4, BEAT), (0, (BEAT/2)), (E4, BEAT), (E4, BEAT), (E4, BEAT), (0, (BEAT/2)), (E4, BEAT), (D4, BEAT), (C4, BEAT), (D4, BEAT), (E4, BEAT), (F4, BEAT), (0, (BEAT/2)), (G4, BEAT), (C4, BEAT), (0, (BEAT/2)), (A4, BEAT), (G4, BEAT), (F4, BEAT), (E4,BEAT), (D4,BEAT), (C4,BEAT)]
correct=[(A0,0.1)]
incorrect=[(C4,0.1),(C4,0.2)]
def setup_gpio():
	wiringpi.wiringPiSetupGpio() # setup wiring pi to use BCM pin numbers
	success = wiringpi.softToneCreate(PIN) # Attempt to set up pin 18
	
	if success != 0:	# If an error is encountered setting up the pin...
		print >> sys.stderr, "Error setting up pin %d (Error Code: %d)." % PIN
		exit(1)

def play_note(note, length=BEAT):
	wiringpi.softToneWrite(PIN, note)
	time.sleep(length)
	wiringpi.softToneWrite(PIN, 0)
	time.sleep(DELAY)

try:
	setup_gpio()
	
#	while True:
#		for n in incorrect:
#			play_note(n[0], n[1])		
#		time.sleep(1)
except KeyboardInterrupt:
	print "User interrupted program."
