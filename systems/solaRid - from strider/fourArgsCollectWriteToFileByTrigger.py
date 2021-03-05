#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## Modification by Phil H Williams
## Add file write and slope trigger

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys

if (len(sys.argv) - 1) < 4:
  print("Need command line arguments, example;")
  print("./scriptName windowSize triggerVal lineCount filename.csv")
  print(sys.argv[0] + " 35 -2.9 6000 outFilename.csv")
  exit(1)

deltaX = int(sys.argv[1])
triggerVal = float(sys.argv[2])
maxReads = int(sys.argv[3])
filename = sys.argv[4]

if maxReads < 6000:
  print(str(maxReads) + " is less than minimum count of data 6000 lines required to run")
  exit(1)

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
slope = 1.1
#deltaX = 45
#triggerVal = -5
counterOn = 'F' # start out as false
linesBeforeTrigger = 1000


#slope = ((y2 -y1)/deltaX)
#print("slope: {}".format(slope))

# read ADC here
count = 1
#for line in dataList:   # This loop is replaced by the analog read loop 
while True:
  #print("Line{}: {}".format(count, line))
  #print("Line{}: {}".format(count, line[0]))
  count = count + 1
  if counterOn == 'F':
    if count == 80000:
      listToFile = []
      #listToFile = listToFile[linesBeforeTrigger:][:]
      count = 1

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
    #if abs(y1 - y2) > 0: 
    #slope = float((y1 - y2)/deltaX)
    slope = (y1 - y2)/deltaX
    #print("slope: {} = {} - {} / {}, count {}".format(slope,y1,y2,deltaX,count))
    #print("slope: %.2f = %d - %d / %d, count %d" % (slope,y1,y2,deltaX,count))
    y2 = y1 

  if slope <= triggerVal:
    counterOn = 'T'
    triggerSlope = slope
    # A trigger occurred start the counter

  if counterOn == 'T':
    readingCount = readingCount + 1
    #print("counter: {} ".format(readingCount))

  #if readingCount >= (maxReads - linesBeforeTrigger)
  if readingCount == (maxReads - linesBeforeTrigger):
    numrows = len(listToFile)
    print "listToFile rows: ", numrows
#    startVal = linesBeforeTrigger + (maxReads - linesBeforeTrigger)
#    if numrows > 4000:
      #subList = listToFile[start:end][]
      #subList = listToFile[2000:][:]
      #startVal = (numrows - 4000) 
#      startVal = (numrows - maxReads) 
 
    #subList = listToFile[startVal:][:]
    subList = listToFile[(numrows - maxReads):][:]
    #print("listToFile rows: ", len(listToFile))
    print "subList rows: ", len(subList)
    #print("counter: {} ".format(readingCount))
    #print("counter: {} ".format(count))
    print("triggerSlope: %.2f" % (triggerSlope))

    # write out last X lines to file and exit
    fileHandle = open(filename, 'w')
    writer = csv.writer(fileHandle)
    writer.writerows(subList)
    fileHandle.close()
    exit(0)

##########################################################
exit(0)


