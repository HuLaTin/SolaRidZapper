#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

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

fileHandle = open("ADC8chan-demofile3.csv", "w")

# Main program loop.
for x in range(30000):
    for i in range(7):
        # The read_adc function will get the value of the specified channel (0-7).
        #values[i] = mcp.read_adc(i)
        fileHandle.write("%d," %(mcp.read_adc(i)))
    fileHandle.write("%d\n" %(mcp.read_adc(7)))

fileHandle.close()


