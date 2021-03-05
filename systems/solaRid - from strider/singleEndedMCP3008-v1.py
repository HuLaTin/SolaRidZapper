#!/usr/bin/python3

import sys

if (len(sys.argv) - 1) < 3:
  print("Need command line arguments, example;")
  print("./scriptName triggerVal lineCount baseFilename.csv")
  print(sys.argv[0] + " 100 8000 outFilename.csv")
  print(sys.argv[0] + " 100 8000 armyWormMothRun1.csv")
  exit(1)

triggerVal = int(sys.argv[1])
maxReads = int(sys.argv[2])
filename = sys.argv[3]

paramsStr = 'params,' + str(triggerVal) + ',' + str(maxReads)
outFile = paramsStr + ',' + filename
print("outFile ", outFile)

if maxReads < 6000:
  print(str(maxReads) + " is less than minimum count of data 6000 lines required to run")
  exit(1)

#exit()

#import time
import csv
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

listToFile = []
readingCount = 0

counterOn = 'F' # start out as false
linesBeforeTrigger = 1000

# create an analog input channel on pin 0 and 1
chanZero = AnalogIn(mcp, 0)
chanOne = AnalogIn(mcp, 1)

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
  #line.append(mcp.read_adc(i))
  line.append(chanZero.value)
  line.append(chanOne.value)

  listToFile.append(line) 
  #numrows = len(listToFile)
  #print("rows: ", numrows)

  #exit()
  #print(" line[0] , ",int(line[0]), "triggerVal ", triggerVal)
  #print(" line[1] , ",int(line[1]))

  if int(line[0]) <= triggerVal:
    counterOn = 'T'
    print(" A trigger occurred start the counter")
    # A trigger occurred start the counter
    print(" line[0] , ",int(line[0]), "triggerVal ", triggerVal)
    #exit(1)

  if counterOn == 'T':
    readingCount = readingCount + 1

  if readingCount == (maxReads - linesBeforeTrigger):
    numrows = len(listToFile)
    print("listToFile rows: ", numrows)
#    startVal = linesBeforeTrigger + (maxReads - linesBeforeTrigger)
#    if numrows > 4000:
      #subList = listToFile[start:end][]
      #subList = listToFile[2000:][:]
      #startVal = (numrows - 4000) 
#      startVal = (numrows - maxReads) 
 
    #subList = listToFile[startVal:][:]
    subList = listToFile[(numrows - maxReads):][:]
    #print("listToFile rows: ", len(listToFile))
    print("subList rows: ", len(subList))

    # write out last X lines to file and exit
    #fileHandle = open(filename, 'w')
    #outFile = paramsStr + ',' + str("%.2f" % round(triggerSlope,2)) + ',' + filename
    fileHandle = open(outFile, 'w')
    writer = csv.writer(fileHandle)
    writer.writerows(subList)
    fileHandle.close()
    exit(0)

######################################################################################
exit(0)


print('Raw ADC Value: ', chan.value)
print('ADC Voltage: ' + str(chan.voltage) + 'V')

print('Raw ADC Value: ', chan.value)
print('ADC Voltage: ' + str(chan.voltage) + 'V')
