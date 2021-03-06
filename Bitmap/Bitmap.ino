

#include "U8glib.h"
#include <String.h>
#include  <SoftwareSerial.h>
#include <AltSoftSerial.h>
AltSoftSerial QRSerial;
//SoftwareSerial QRSerial(8,9); // RX 、 TX
unsigned long curtime=0;
int interval =3000; 
char disp[4];
U8GLIB_ST7920_128X64_4X u8g(13, 11, 10);  // SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
int scan=0;
const unsigned char bitmap_zero[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};


const unsigned char bitmap_one[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x07,0xE0, // .....######.....
  0x07,0xE0, // .....######.....
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_two[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x1F,0xE0, // ...########.....
  0x1F,0xE0, // ...########.....
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_three[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_four[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x01,0xE0, // .......####.....
  0x01,0xE0, // .......####.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x1F,0xF8, // ...##########...
  0x1F,0xF8, // ...##########...
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_five[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0xE0, // .....######.....
  0x07,0xE0, // .....######.....
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_six[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x18,0x00, // ...##...........
  0x18,0x00, // ...##...........
  0x1F,0x80, // ...######.......
  0x1F,0x80, // ...######.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_seven[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x1F,0xE0, // ...########.....
  0x1F,0xE0, // ...########.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_eight[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};

const unsigned char bitmap_nine[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x07,0x80, // .....####.......
  0x07,0x80, // .....####.......
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x18,0x60, // ...##....##.....
  0x07,0xE0, // .....######.....
  0x07,0xE0, // .....######.....
  0x00,0x60, // .........##.....
  0x00,0x60, // .........##.....
  0x01,0x80, // .......##.......
  0x01,0x80, // .......##.......
  0x06,0x00, // .....##.........
  0x06,0x00, // .....##.........
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};


const unsigned char bitmap_sharp[] PROGMEM = {
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x1F,0xF8, // ...##########...
  0x1F,0xF8, // ...##########...
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x1F,0xF8, // ...##########...
  0x1F,0xF8, // ...##########...
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x06,0x60, // .....##..##.....
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00, // ................
  0x00,0x00  // ................
};


const unsigned char bitmap_check[] PROGMEM = {
  0x00,0x00,0x00, // ........................
  0x00,0x00,0x00, // ........................
  0x00,0x7E,0x00, // .........######.........
  0x01,0xFF,0x80, // .......##########.......
  0x07,0xFF,0xE0, // .....##############.....
  0x0F,0xFF,0xF0, // ....################....
  0x0F,0xFF,0xF0, // ....################....
  0x1F,0xFF,0xF8, // ...##################...
  0x1F,0xFF,0x38, // ...#############..###...
  0x3F,0xFE,0x3C, // ..#############...####..
  0x3F,0xFC,0x7C, // ..############...#####..
  0x3F,0xF8,0xFC, // ..###########...######..
  0x3C,0xF1,0xFC, // ..####..####...#######..
  0x3C,0x63,0xFC, // ..####...##...########..
  0x3E,0x07,0xFC, // ..#####......#########..
  0x1F,0x0F,0xF8, // ...#####....#########...
  0x1F,0x9F,0xF8, // ...######..##########...
  0x0F,0xFF,0xF0, // ....################....
  0x0F,0xFF,0xF0, // ....################....
  0x07,0xFF,0xE0, // .....##############.....
  0x01,0xFF,0x80, // .......##########.......
  0x00,0x7E,0x00, // .........######.........
  0x00,0x00,0x00, // ........................
  0x00,0x00,0x00  // ........................
};

const unsigned char bitmap_text[] PROGMEM = {
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x03,0xC0,0xFF,0xF0,0x00,0x3F,0xFF,0xFC,0x00,0x00,0xF0,0xF0,0x00,0x00,0x0F,0x00, // ......####......############..............####################..................####....####........................####........
  0x03,0xC0,0xFF,0xF0,0x00,0x3F,0xFF,0xFC,0x00,0x00,0xF0,0xF0,0x00,0x00,0x0F,0x00, // ......####......############..............####################..................####....####........................####........
  0x3F,0xFC,0xFF,0xF0,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC,0x3F,0xFC,0x0F,0x00, // ..############..############........####..####################....############################....############......####........
  0x3F,0xFC,0xFF,0xF0,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC,0x3F,0xFC,0x0F,0x00, // ..############..############........####..####################....############################....############......####........
  0x3F,0xFC,0x00,0xF0,0x0F,0x3C,0xCF,0x3C,0x3F,0xFF,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC, // ..############..........####........####..####..##..####..####....############################....############################..
  0x3F,0xFC,0x00,0xF0,0x0F,0x3C,0xCF,0x3C,0x3F,0xFF,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC, // ..############..........####........####..####..##..####..####....############################....############################..
  0x3C,0x3C,0xFF,0xFC,0x00,0x3F,0xFF,0xFC,0x3C,0x00,0x3C,0x00,0x03,0xC3,0xFF,0xFC, // ..####....####..##############............####################....####............####................####....################..
  0x3C,0x3C,0xFF,0xFC,0x00,0x3F,0xFF,0xFC,0x3C,0x00,0x3C,0x00,0x03,0xC3,0xFF,0xFC, // ..####....####..##############............####################....####............####................####....################..
  0x3F,0xFC,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC,0x3C,0x00,0x3C,0x00,0x03,0xC0,0x3C,0x3C, // ..############..##############....######..####################....####............####................####........####....####..
  0x3F,0xFC,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC,0x3C,0x00,0x3C,0x00,0x03,0xC0,0x3C,0x3C, // ..############..##############....######..####################....####............####................####........####....####..
  0x3F,0xFC,0x00,0xF0,0x3F,0x3C,0x00,0x3C,0x3C,0x00,0x0F,0x3C,0x03,0xC0,0x3C,0x3C, // ..############..........####......######..####............####....####..............####..####........####........####....####..
  0x3F,0xFC,0x00,0xF0,0x3F,0x3C,0x00,0x3C,0x3C,0x00,0x0F,0x3C,0x03,0xC0,0x3C,0x3C, // ..############..........####......######..####............####....####..............####..####........####........####....####..
  0x3C,0x3F,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0x0F,0xFC,0x03,0xC0,0x3C,0x3C, // ..####....####################......####..####################....##############....##########........####........####....####..
  0x3C,0x3F,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0x0F,0xFC,0x03,0xC0,0x3C,0x3C, // ..####....####################......####..####################....##############....##########........####........####....####..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0x0F,0xF0,0x03,0xC0,0xF0,0x3C, // ..############################......####..####################....##############....########..........####......####......####..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFF,0x0F,0xF0,0x03,0xC0,0xF0,0x3C, // ..############################......####..####################....##############....########..........####......####......####..
  0x3F,0xC3,0xCF,0x3C,0x0F,0x03,0xFC,0x3C,0x3C,0x0F,0x03,0xC0,0x03,0xC0,0xF0,0x3C, // ..########....####..####..####......####......########....####....####......####......####............####......####......####..
  0x3F,0xC3,0xCF,0x3C,0x0F,0x03,0xFC,0x3C,0x3C,0x0F,0x03,0xC0,0x03,0xC0,0xF0,0x3C, // ..########....####..####..####......####......########....####....####......####......####............####......####......####..
  0x03,0xFF,0xFF,0xFC,0x3C,0x0F,0xFF,0xFC,0x3C,0x0F,0x0F,0xC0,0x03,0xC0,0xF0,0x3C, // ......########################....####......##################....####......####....######............####......####......####..
  0x03,0xFF,0xFF,0xFC,0x3C,0x0F,0xFF,0xFC,0x3C,0x0F,0x0F,0xC0,0x03,0xC0,0xF0,0x3C, // ......########################....####......##################....####......####....######............####......####......####..
  0x3F,0xFF,0xFF,0xFC,0x3C,0x3F,0xF3,0xF0,0x3C,0x0F,0x0F,0xF0,0x3F,0xFF,0xC0,0x3C, // ..############################....####....##########..######......####......####....########......################........####..
  0x3F,0xFF,0xFF,0xFC,0x3C,0x3F,0xF3,0xF0,0x3C,0x0F,0x0F,0xF0,0x3F,0xFF,0xC0,0x3C, // ..############################....####....##########..######......####......####....########......################........####..
  0x3F,0xC3,0xCF,0x3C,0x3C,0x3C,0xF0,0xFC,0x3C,0x0F,0x3F,0xF0,0x3F,0xFF,0xC0,0x3C, // ..########....####..####..####....####....####..####....######....####......####..##########......################........####..
  0x3F,0xC3,0xCF,0x3C,0x3C,0x3C,0xF0,0xFC,0x3C,0x0F,0x3F,0xF0,0x3F,0xFF,0xC0,0x3C, // ..########....####..####..####....####....####..####....######....####......####..##########......################........####..
  0x3F,0xFF,0xCF,0x3C,0x3F,0xFF,0xF0,0x3C,0x3C,0xFF,0xFC,0x3C,0x00,0x03,0xC3,0xFC, // ..################..####..####....##################......####....####..##############....####................####....########..
  0x3F,0xFF,0xCF,0x3C,0x3F,0xFF,0xF0,0x3C,0x3C,0xFF,0xFC,0x3C,0x00,0x03,0xC3,0xFC, // ..################..####..####....##################......####....####..##############....####................####....########..
  0x0F,0xFC,0x0F,0x00,0x3F,0xFF,0xFF,0xFC,0x3C,0xFC,0xF0,0x3C,0x00,0x03,0xC3,0xF0, // ....##########......####..........############################....####..######..####......####................####....######....
  0x0F,0xFC,0x0F,0x00,0x3F,0xFF,0xFF,0xFC,0x3C,0xFC,0xF0,0x3C,0x00,0x03,0xC3,0xF0, // ....##########......####..........############################....####..######..####......####................####....######....
  0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xFC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ..................................................############..................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xFC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00  // ..................................................############..................................................................
};

const unsigned char bitmap_error[] PROGMEM = {
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x03,0x30,0x00,0x0F,0xF0,0x0C,0x33,0x03,0xC3,0xF0,0x00,0x00,0x00, // ..............................##..##................########........##....##..##......####....######............................
  0x00,0x00,0x00,0x03,0x30,0x00,0x0F,0xF0,0x0C,0x33,0x03,0xC3,0xF0,0x00,0x00,0x00, // ..............................##..##................########........##....##..##......####....######............................
  0x00,0x18,0x00,0x03,0x3F,0x03,0xFC,0xC0,0x33,0xFF,0x00,0x03,0x30,0x00,0x18,0x00, // ...........##.................##..######......########..##........##..##########..............##..##...............##...........
  0x00,0x3C,0x00,0x03,0x3F,0x03,0xFC,0xC0,0x33,0xFF,0x00,0x03,0x30,0x00,0x3C,0x00, // ..........####................##..######......########..##........##..##########..............##..##..............####..........
  0x00,0x3C,0x00,0x0C,0xF3,0x00,0xCF,0xF0,0x00,0x33,0x03,0xF3,0x30,0x00,0x3C,0x00, // ..........####..............##..####..##........##..########..............##..##......######..##..##..............####..........
  0x00,0x7E,0x00,0x0C,0xF3,0x00,0xCF,0xF0,0x00,0x33,0x03,0xF3,0x30,0x00,0x7E,0x00, // .........######.............##..####..##........##..########..............##..##......######..##..##.............######.........
  0x00,0xFF,0x00,0x0F,0x0C,0x00,0xCC,0xC0,0x3F,0x33,0x00,0x33,0xF0,0x00,0xFF,0x00, // ........########............####....##..........##..##..##........######..##..##..........##..######............########........
  0x00,0xFF,0x00,0x0F,0x0C,0x00,0xCC,0xC0,0x3F,0x33,0x00,0x33,0xF0,0x00,0xFF,0x00, // ........########............####....##..........##..##..##........######..##..##..........##..######............########........
  0x01,0xFF,0x80,0x3F,0xF3,0x00,0xCF,0xF0,0x0C,0xFF,0x03,0xF0,0x00,0x01,0xFF,0x80, // .......##########.........##########..##........##..########........##..########......######...................##########.......
  0x01,0xE7,0x80,0x3F,0xF3,0x00,0xCF,0xF0,0x0C,0xFF,0x03,0xF0,0x00,0x01,0xE7,0x80, // .......####..####.........##########..##........##..########........##..########......######...................####..####.......
  0x03,0xE7,0xC0,0x0F,0x0C,0x03,0x0C,0xC0,0x3F,0x00,0x00,0x3F,0xC0,0x03,0xE7,0xC0, // ......#####..#####..........####....##........##....##..##........######..................########............#####..#####......
  0x07,0xE7,0xE0,0x0F,0x0C,0x03,0x0C,0xC0,0x3F,0x00,0x00,0x3F,0xC0,0x07,0xE7,0xE0, // .....######..######.........####....##........##....##..##........######..................########...........######..######.....
  0x07,0xE7,0xE0,0x0F,0xFF,0x00,0xFF,0xF0,0x0C,0x3F,0x03,0xF1,0xC0,0x07,0xE7,0xE0, // .....######..######.........############........############........##....######......######...###...........######..######.....
  0x0F,0xFF,0xF0,0x0F,0xFF,0x00,0xFF,0xF0,0x0C,0x3F,0x03,0xC1,0xC0,0x0F,0xFF,0xF0, // ....################........############........############........##....######......####.....###..........################....
  0x0F,0xFF,0xF0,0x0F,0x0C,0x00,0xCC,0x30,0x3F,0x33,0x00,0x7F,0xF0,0x0F,0xFF,0xF0, // ....################........####....##..........##..##....##......######..##..##.........###########........################....
  0x1F,0xE7,0xF8,0x0F,0x0C,0x00,0xCC,0x30,0x3F,0x33,0x00,0x7F,0xF0,0x1F,0xE7,0xF8, // ...########..########.......####....##..........##..##....##......######..##..##.........###########.......########..########...
  0x3F,0xE7,0xFC,0x0F,0x3C,0x00,0xCF,0x30,0x3C,0x3F,0x03,0xC0,0x00,0x3F,0xE7,0xFC, // ..#########..#########......####..####..........##..####..##......####....######......####................#########..#########..
  0x3F,0xFF,0xFC,0x0F,0x3C,0x00,0xCF,0x30,0x3C,0x3F,0x03,0xC0,0x00,0x3F,0xFF,0xFC, // ..####################......####..####..........##..####..##......####....######......####................####################..
  0x3F,0xFF,0xFC,0x0C,0xCF,0x00,0xFC,0x30,0x0F,0x33,0x03,0xCC,0xC0,0x3F,0xFF,0xFC, // ..####################......##..##..####........######....##........####..##..##......####..##..##........####################..
  0x1F,0xFF,0xF8,0x0C,0xCF,0x00,0xFC,0x30,0x0F,0x33,0x03,0xCC,0xC0,0x1F,0xFF,0xF8, // ...##################.......##..##..####........######....##........####..##..##......####..##..##.........##################...
  0x00,0x00,0x00,0x0C,0x0C,0x00,0x00,0xF0,0x3C,0x3F,0x03,0xF0,0x30,0x00,0x00,0x00, // ............................##......##..................####......####....######......######......##............................
  0x00,0x00,0x00,0x0C,0x0C,0x00,0x00,0xF0,0x3C,0x3F,0x03,0xF0,0x30,0x00,0x00,0x00, // ............................##......##..................####......####....######......######......##............................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x03,0xC0,0x00,0x00,0x3C,0x00,0x3C,0x00,0x03,0xC0,0xFF,0xF0,0x00,0x3F,0xFF,0xFC, // ......####........................####............####................####......############..............####################..
  0x03,0xC0,0x00,0x00,0x3C,0x00,0x3C,0x00,0x03,0xC0,0xFF,0xF0,0x00,0x3F,0xFF,0xFC, // ......####........................####............####................####......############..............####################..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x00,0x3C,0x00,0x3F,0xFC,0xFF,0xF0,0x0F,0x3F,0xFF,0xFC, // ....##########################....######..........####............############..############........####..####################..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x00,0x3C,0x00,0x3F,0xFC,0xFF,0xF0,0x0F,0x3F,0xFF,0xFC, // ....##########################....######..........####............############..############........####..####################..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFC,0x00,0xF0,0x0F,0x3C,0xCF,0x3C, // ..############################......####..####################....############..........####........####..####..##..####..####..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC,0x3F,0xFC,0x00,0xF0,0x0F,0x3C,0xCF,0x3C, // ..############################......####..####################....############..........####........####..####..##..####..####..
  0x3F,0xCF,0x3C,0xF0,0x00,0x3F,0xFF,0xFC,0x3C,0x3C,0xFF,0xFC,0x00,0x3F,0xFF,0xFC, // ..########..####..####..####..............####################....####....####..##############............####################..
  0x3F,0xCF,0x3C,0xF0,0x00,0x3F,0xFF,0xFC,0x3C,0x3C,0xFF,0xFC,0x00,0x3F,0xFF,0xFC, // ..########..####..####..####..............####################....####....####..##############............####################..
  0x03,0xCF,0x3C,0xF0,0x3C,0x00,0x3C,0x00,0x3F,0xFC,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC, // ......####..####..####..####......####............####............############..##############....######..####################..
  0x03,0xCF,0x3C,0xF0,0x3C,0x00,0x3C,0x00,0x3F,0xFC,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC, // ......####..####..####..####......####............####............############..##############....######..####################..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x00,0x3C,0x00,0x3F,0xFC,0x00,0xF0,0x3F,0x3C,0x00,0x3C, // ....##########################....######..........####............############..........####......######..####............####..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x00,0x3C,0x00,0x3F,0xFC,0x00,0xF0,0x3F,0x3C,0x00,0x3C, // ....##########################....######..........####............############..........####......######..####............####..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC,0x3C,0x3F,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC, // ....##########################....######..####################....####....####################......####..####################..
  0x0F,0xFF,0xFF,0xFC,0x3F,0x3F,0xFF,0xFC,0x3C,0x3F,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC, // ....##########################....######..####################....####....####################......####..####################..
  0x03,0xCF,0x3C,0xF0,0x00,0x3F,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC, // ......####..####..####..####..............####################....############################......####..####################..
  0x03,0xCF,0x3C,0xF0,0x00,0x3F,0xFF,0xFC,0x3F,0xFF,0xFF,0xFC,0x0F,0x3F,0xFF,0xFC, // ......####..####..####..####..............####################....############################......####..####################..
  0x03,0xCF,0x3C,0xF0,0x0F,0x03,0xC0,0x00,0x3F,0xC3,0xCF,0x3C,0x0F,0x03,0xFC,0x3C, // ......####..####..####..####........####......####................########....####..####..####......####......########....####..
  0x03,0xCF,0x3C,0xF0,0x0F,0x03,0xC0,0x00,0x3F,0xC3,0xCF,0x3C,0x0F,0x03,0xFC,0x3C, // ......####..####..####..####........####......####................########....####..####..####......####......########....####..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x0F,0x00,0xF0,0x03,0xFF,0xFF,0xFC,0x3C,0x0F,0xFF,0xFC, // ..############################......####....####........####..........########################....####......##################..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x0F,0x00,0xF0,0x03,0xFF,0xFF,0xFC,0x3C,0x0F,0xFF,0xFC, // ..############################......####....####........####..........########################....####......##################..
  0x3F,0xFF,0xFF,0xFC,0x0F,0x0F,0x00,0xF0,0x3F,0xFF,0xFF,0xFC,0x3C,0x3F,0xF3,0xF0, // ..############################......####....####........####......############################....####....##########..######....
  0x3F,0xFF,0xFF,0xFC,0x0F,0x0F,0x00,0xF0,0x3F,0xFF,0xFF,0xFC,0x3C,0x3F,0xF3,0xF0, // ..############################......####....####........####......############################....####....##########..######....
  0x03,0xCF,0x3C,0xF0,0x3C,0x3C,0x00,0xF0,0x3F,0xC3,0xCF,0x3C,0x3C,0x3C,0xF0,0xFC, // ......####..####..####..####......####....####..........####......########....####..####..####....####....####..####....######..
  0x03,0xCF,0x3C,0xF0,0x3C,0x3C,0x00,0xF0,0x3F,0xC3,0xCF,0x3C,0x3C,0x3C,0xF0,0xFC, // ......####..####..####..####......####....####..........####......########....####..####..####....####....####..####....######..
  0x0F,0xC3,0xCF,0x3C,0x3C,0x3F,0xFF,0xFC,0x3F,0xFF,0xCF,0x3C,0x3F,0xFF,0xF0,0x3C, // ....######....####..####..####....####....####################....################..####..####....##################......####..
  0x0F,0xC3,0xCF,0x3C,0x3C,0x3F,0xFF,0xFC,0x3F,0xFF,0xCF,0x3C,0x3F,0xFF,0xF0,0x3C, // ....######....####..####..####....####....####################....################..####..####....##################......####..
  0x0F,0x03,0xCF,0x3C,0x3C,0x3F,0xFF,0xFC,0x0F,0xFC,0x0F,0x00,0x3F,0xFF,0xFF,0xFC, // ....####......####..####..####....####....####################......##########......####..........############################..
  0x0F,0x03,0xCF,0x3C,0x3C,0x3F,0xFF,0xFC,0x0F,0xFC,0x0F,0x00,0x3F,0xFF,0xFF,0xFC, // ....####......####..####..####....####....####################......##########......####..........############################..
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xFC, // ..................................................................................................................############..
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xFC, // ..................................................................................................................############..
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // ................................................................................................................................
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00  // ................................................................................................................................
};

void drawURL(void)
{
  u8g.setFont(u8g_font_gdr12);
  
  u8g.drawStr(60,30,"1236");
  
}
void drawOne(void)
{
  u8g.drawBitmapP( 40, 2, 2, 24, bitmap_zero);
  
}
void draw(void) {
  
  if(scan==1)
  {
    
    // graphic commands to redraw the complete screen should be placed here  
  u8g.drawBitmapP( 0, 2, 3, 24, bitmap_check);
  u8g.drawBitmapP( 24, 2, 2, 24, bitmap_sharp);
  switch(disp[0]){
    case '0': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_zero);break;
    case '1': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_one); break;
    case '2': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_two); break;
    case '3': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_three); break;
    case '4': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_four); break;
    case '5': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_five); break;
    case '6': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_six); break;
    case '7': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_seven); break;
    case '8': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_eight); break;
    case '9': u8g.drawBitmapP( 40, 2, 2, 24, bitmap_nine); break;
    default:drawOne;
  }
  switch(disp[1]){
    case '0': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_zero);break;
    case '1': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_one); break;
    case '2': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_two); break;
    case '3': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_three); break;
    case '4': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_four); break;
    case '5': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_five); break;
    case '6': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_six); break;
    case '7': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_seven); break;
    case '8': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_eight); break;
    case '9': u8g.drawBitmapP( 56, 2, 2, 24, bitmap_nine); break;
  }
  switch(disp[2]){
    case '0': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_zero);break;
    case '1': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_one); break;
    case '2': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_two); break;
    case '3': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_three); break;
    case '4': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_four); break;
    case '5': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_five); break;
    case '6': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_six); break;
    case '7': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_seven); break;
    case '8': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_eight); break;
    case '9': u8g.drawBitmapP( 72, 2, 2, 24, bitmap_nine); break;
  }
  switch(disp[3]){
    case '0': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_zero);break;
    case '1': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_one); break;
    case '2': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_two); break;
    case '3': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_three); break;
    case '4': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_four); break;
    case '5': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_five); break;
    case '6': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_six); break;
    case '7': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_seven); break;
    case '8': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_eight); break;
    case '9': u8g.drawBitmapP( 88, 2, 2, 24, bitmap_nine); break;
  }
  u8g.drawBitmapP( 104, 2, 3, 24, bitmap_check);
  u8g.drawBitmapP( 0, 30, 16, 32, bitmap_text);
  
  }
 
}

void setup(void) {
  Serial.begin(9600);
  QRSerial.begin(57600);
}

void loop(void) {
  
  // picture loop
  char c=' ';
  String data="";
  u8g.firstPage();  
  do {
    draw();
    //drawURL();
  } while( u8g.nextPage() );
  
  while(QRSerial.available())
{
  c=QRSerial.read();
  Serial.write(c);
  data+=c;
  if(!QRSerial.available())
    Serial.println();
   

}
if(data!="\0")
{
  scan=1;
  curtime=millis();
 // Serial.println(data);
 // Serial.println(data.length());
char datachar[data.length()+1];
data.toCharArray(datachar,data.length()+1);
for(int i=25;datachar[i]!='\0';i++)
{
//Serial.print(datachar[i]); // 25-28
disp[i-25]=datachar[i];
//Serial.print(disp[i-25]); // 25-28
//Serial.println();
}
  // rebuild the picture after some delay
  
}
if(millis()-curtime>interval)
{
  if(scan==1)
  scan=0;
}
}
