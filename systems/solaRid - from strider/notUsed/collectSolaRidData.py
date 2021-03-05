#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## mode by Phil H Williams

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys

if (len(sys.argv) - 1) == 0:
  print("Need command line arguments, example;")
  print("./scriptName lineCount filename.csv")
  print(sys.argv[0] + " 3000 outFilename.csv")
  exit(1)

lineCount = int(sys.argv[1])
filename = sys.argv[2]
#print "line count ", lineCount 

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

#fileHandle = open("ADC8chan-demofile3.csv", "w")
fileHandle = open(filename, "w")

# Main program loop.
for x in range(lineCount):
    for i in range(7):
        # The read_adc function will get the value of the specified channel (0-7).
        #values[i] = mcp.read_adc(i)
        fileHandle.write("%d," %(mcp.read_adc(i)))
    fileHandle.write("%d\n" %(mcp.read_adc(7)))

fileHandle.close()


