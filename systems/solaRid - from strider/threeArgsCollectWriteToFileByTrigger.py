#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## Modification by Phil H Williams
## Add file write and slope trigger

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys

if (len(sys.argv) - 1) < 3:
  print("Need command line arguments, example;")
  print("./scriptName triggerVal lineCount filename.csv")
  print(sys.argv[0] + " -4.4 3000 outFilename.csv")
  exit(1)

#lineCount = int(sys.argv[1])
triggerVal = float(sys.argv[1])
maxReads = int(sys.argv[2])
filename = sys.argv[3]

import time
import csv
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

listToFile = []
readingCount = 0

## slope = ((Y2 - Y1)/(X2 - X1))
#y1 = 401
y2 = 400
deltaX = 45
slope = 1
#triggerVal = -5
counterOn = 'F' # start out as false

#slope = ((y2 -y1)/deltaX)
#print("slope: {}".format(slope))

# read ADC here
count = 1
#for line in dataList:   # This loop is replaced by the analog read loop 
while True:
  #print("Line{}: {}".format(count, line))
  #print("Line{}: {}".format(count, line[0]))
  count = count + 1
  if count >= 8000:
    listToFile = []

#  exit()
  line = []
  # read ADC here
  for i in range(8):
#    print("i {}".format(i))
    line.append(mcp.read_adc(i))

  listToFile.append(line) 
  #numrows = len(listToFile)
  #print("rows: ", numrows)

  if (count % deltaX) == 0:
    #print("Line{}: {}".format(count, line[0]))
    #print("Line{}".format(count))
    y1 = int(line[0]) 
    if (y1 - y2) > 0: 
      slope = ((y1 - y2)/deltaX)
    y2 = y1 

  if slope < triggerVal:
    counterOn = 'T'
    print("slope: {} = {} - {} / {}, count {}".format(slope,y1,y2,deltaX,count))
    #print("trigger by slope: {} ".format(slope))
    # A trigger occurred start the counter

  if counterOn == 'T':
    readingCount = readingCount + 1
    #print("counter: {} ".format(readingCount))

  if readingCount >= maxReads:
    # write out last X lines to file and exit
    fileHandle = open(filename, 'w')
    numrows = len(listToFile)
    print "rows: ", numrows
    startVal = 2000 
    if numrows > 2000:
      #subList = listToFile[start:end][]
      #subList = listToFile[2000:][:]
      startVal = (numrows - 4000) 
 
    subList = listToFile[startVal:][:]
#    print("subList rows: ", len(subList))
    print "subList rows: ", len(subList)
    print("counter: {} ".format(readingCount))

    writer = csv.writer(fileHandle)
    writer.writerows(subList)
    fileHandle.close()
    exit(0)

##########################################################
exit(0)


