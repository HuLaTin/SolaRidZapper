#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## Modification by Phil H Williams
## Add file write

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys

if (len(sys.argv) - 1) < 2:
  print("Need command line arguments, example;")
  print("./scriptName lineCount filename.csv")
  print(sys.argv[0] + " 3000 outFilename.csv")
  exit(1)

lineCount = int(sys.argv[1])
filename = sys.argv[2]

import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

fileHandle = open(filename, "w")

fileHandle.write("%d\n" % (time.time()))

# Main program loop.
for x in range(lineCount):
    for i in range(7):
        fileHandle.write("%d," %(mcp.read_adc(i)))
    fileHandle.write("%d\n" %(mcp.read_adc(7)))

fileHandle.write("%d\n" % (time.time()))
fileHandle.close()

