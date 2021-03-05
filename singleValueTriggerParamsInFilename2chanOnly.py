#!/usr/bin/python

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## Modification by Phil H Williams
## Add file write and trigger

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys

if (len(sys.argv) - 1) < 3:
  print("Need command line arguments, example;")
  print("./scriptName triggerVal lineCount baseFilename.csv")
  print(sys.argv[0] + " 100 8000 outFilename.csv")
  print(sys.argv[0] + " 100 8000 armyWormMothRun1.csv")
  exit(1)

#deltaX = int(sys.argv[1])
triggerVal = int(sys.argv[1])
maxReads = int(sys.argv[2])
filename = sys.argv[3]

#paramsStr = 'params,' + str(deltaX) + ',' + str(triggerVal) + ',' + str(maxReads)
paramsStr = 'params,' + str(triggerVal) + ',' + str(maxReads)
#outFile = 'params,' + str(deltaX) + ',' + str(triggerVal) + ',' + str(maxReads) + ',*,' + filename
outFile = paramsStr + ',' + filename
print "outFile ", outFile

#exit()

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

counterOn = 'F' # start out as false
linesBeforeTrigger = 1000

# read ADC here
count = 1
#for line in dataList:   # This loop is replaced by the analog read loop 
while True:
  #print("Line{}: {}".format(count, line))
  #print("Line{}: {}".format(count, line[0]))
  count = count + 1
  if counterOn == 'F':
    if count == 5000:
      listToFile = []
      #listToFile = listToFile[linesBeforeTrigger:][:]
      count = 1

#  exit()
  line = []
  # read ADC here
  for i in range(2):
#    print("i {}".format(i))
    line.append(mcp.read_adc(i))

  listToFile.append(line) 
  #numrows = len(listToFile)
  #print("rows: ", numrows)

  if int(line[0]) <= triggerVal:
    counterOn = 'T'
    print(" A trigger occurred start the counter")
    # A trigger occurred start the counter
    #print(" line[0] , ",int(line[0]), "triggerVal ", triggerVal)
    #exit(1)

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
    #print("triggerSlope: %.2f" % (triggerSlope))

    # write out last X lines to file and exit
    #fileHandle = open(filename, 'w')
    #outFile = paramsStr + ',' + str("%.2f" % round(triggerSlope,2)) + ',' + filename
    fileHandle = open(outFile, 'w')
    writer = csv.writer(fileHandle)
    writer.writerows(subList)
    fileHandle.close()
    exit(0)

##########################################################
exit(0)


