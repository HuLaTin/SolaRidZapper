#!/usr/bin/python3

import sys
import time, csv, os, requests, random, string
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from urllib.request import urlopen
from lxml import etree
from numpy import mean

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

listToFile = []
count = 0
outFile = str(datetime.datetime.now()) + "-zapLongTest.csv"

try:
    while True:
        count = count + 1
        #print(count)
        line = []
        for i in range(2):
            line.append(mcp.read_adc(i))
        listToFile.append(line)

        if count == 10000:
            #print("writing")
            fileHandle = open(outFile, 'a')
            writer = csv.writer(fileHandle)
            writer.writerows(listToFile)
            fileHandle.close()
            listToFile = []
            count = 0


except KeyboardInterrupt:
    print("KeyboardInterrupt")
    fileHandle = open(outFile, 'a')
    writer = csv.writer(fileHandle)
    writer.writerows(listToFile)
    fileHandle.close()
    exit(0)