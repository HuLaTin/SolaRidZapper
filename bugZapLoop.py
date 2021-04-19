#!/usr/bin/python3

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
## Modification by Phil H Williams
## Hunter Tiner
## Add file write and slope trigger

## https://www.instructables.com/id/ADC-MCP3008-Raspberry-Pi/

import sys
#import lxml.html

if (len(sys.argv) - 1) < 2:
  print("Need command line arguments, example;")
  print("./scriptName triggerVal lineCount")
  print(sys.argv[0] + " 100 10000")
  #print(sys.argv[0] + " 100 10000 armyWormMothRun1.csv")
  exit(1)

import RPi.GPIO as GPIO
outputPort = int(18)
#######
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(outputPort,GPIO.OUT)
#######

if GPIO.input(outputPort) == GPIO.HIGH:
    print("LED is already on! Reset, and try again!")
    exit(1)

import time, csv, os, requests, random, string
import datetime

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from urllib.request import urlopen
from lxml import etree
#import LED

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# login for webscraping
loginData = {'mailuid':'rice', 'pwd':'rice','login-submit':''}
r = requests.post('http://69.4.196.7/solarid/includes/login.inc.php', loginData)
html = etree.HTML(r.text)

triggerVal = int(sys.argv[1])
maxReads = int(sys.argv[2])
#filename = sys.argv[3]
#timeStamp = str(time.time_ns())

#GloveBox SolaRid Zapper #43, change this value for others.
webSensorID = 43

if maxReads < 8000:
  print(str(maxReads) + " is less than minimum count of data 8000 lines required to run")
  exit(1)


linesBeforeTrigger = 2000

while True:
  listToFile = []
  readingCount = 0
  counterOn = False # start out as false
  if GPIO.input(outputPort) == GPIO.LOW:
    #collect metaData and set filenames
    find = etree.XPath("//table/tr[td[1]/text() = "+ str(webSensorID) +"]/td/text()")
    metaData = [triggerVal, maxReads, find(html)]

    now = datetime.datetime.now()
    today = datetime.date.today()


    ident = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    outFile = today.strftime("%Y%b%d") + "-" + ident + ".csv"
    metaOutFile = today.strftime("%Y%b%d") + "-" + ident + "-M.csv"

    outFile = os.path.join("bugZapRuns", outFile)
    metaOutFile = os.path.join("bugZapRuns", metaOutFile)

    print("outFile -", outFile)

    # read ADC here
    count = 1
    #for line in dataList:   # This loop is replaced by the analog read loop
    while True:
      count = count + 1
      if counterOn == False:
        if count == 10000:
          listToFile = []
          count = 1

      line = []
      # read ADC here
      for i in range(2):
        line.append(mcp.read_adc(i))

      listToFile.append(line)

      if int(line[0]) <= triggerVal and counterOn != True:
        counterOn = True
        startTime = time.time_ns()
        # Turn LED on #
        GPIO.output(outputPort,GPIO.HIGH)
        ################
        print("A trigger occurred! starting the counter.")

      if counterOn == True:
        readingCount = readingCount + 1

      if readingCount == (maxReads - linesBeforeTrigger):
        #endTime = time.time_ns()
        times = [startTime, time.time_ns()]
        metaData = metaData + times

        ### Turn LED off ###
        numrows = len(listToFile)
        subList = listToFile[(numrows - maxReads):][:]

        print("listToFile rows: ", numrows)
        print("subList rows: ", len(subList))

        fileHandle = open(outFile, 'w')
        writer = csv.writer(fileHandle)
        writer.writerows(subList)
        fileHandle.close()

        f = open(metaOutFile, 'w')
        f.write(str(metaData))
        f.close()

        GPIO.output(outputPort,GPIO.HIGH)
        
        f = open("ident.dat", 'w')
        f.write(str(ident))
        f.close()
        #Wait for sister pi to turn off
        break
  else:
    print("Waiting for LED off.")
    time.sleep(15)
##########################################################





