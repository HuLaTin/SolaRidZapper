#!/usr/bin/python3

import csv
#import numpy as np

#analogList = []
listToFile = []
maxReads = 3000
readingCount = 0

#with open('forSlopeCalc.csv', newline='') as f:
with open('zap6000dataSubset.csv', newline='') as f:
  reader = csv.reader(f)
  dataList = list(reader)
f.close()

#print(analogList)

## slope = ((Y2 - Y1)/(X2 - X1))
#y1 = 401
y2 = 400
deltaX = 45
slope = 1
triggerVal = -5
counterOn = 'F' # start out as false

#slope = ((y2 -y1)/deltaX)
#print("slope: {}".format(slope))

count = 1
for line in dataList:   # This loop is replaced by the analog read loop 
  #print("Line{}: {}".format(count, line))
  #print("Line{}: {}".format(count, line[0]))
  count = count + 1
  if count >= 8000:
    listToFile = []

  listToFile.append(line) 
  #numrows = len(listToFile)
  #print("rows: ", numrows)

  if (count % deltaX) == 0:
    #print("Line{}: {}".format(count, line[0]))
    #print("Line{}".format(count))
    y1 = int(line[0])  
    slope = ((y1 - y2)/deltaX)
    #print("slope: {} = {} - {} / {} ".format(slope,y1,y2,50))
    y2 = y1 

  if slope < triggerVal:
    counterOn = 'T'
    #print("trigger by slope: {} ".format(slope))
    # A trigger occurred start the counter

  if counterOn == 'T':
    readingCount = readingCount + 1
    #print("counter: {} ".format(readingCount))

  if readingCount >= maxReads:
    # write out last 8,000 lines to file and exit
    fileHandle = open("subListOut.csv",'w')
    writer = csv.writer(fileHandle)
    numrows = len(listToFile)
    print("rows: ", numrows)
    startVal = 2000 
    if numrows > 2000:
      #subList = listToFile[start:end][]
      #subList = listToFile[2000:][:]
      startVal = (numrows - 4000) 
 
    subList = listToFile[startVal:][:]
    print("subList rows: ", len(subList))

    writer.writerows(subList)
    fileHandle.close()
    exit(0)

##########################################################
exit(0)


