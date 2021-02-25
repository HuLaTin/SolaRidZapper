import math
import time
import csv
import datetime
import numpy as np
from grove.adc import ADC
import requests
import lxml.html
from urllib.request import urlopen
from lxml import etree

loginData = {'mailuid':'rice', 'pwd':'rice','login-submit':''}
r = requests.post('http://69.4.196.7/solarid/includes/login.inc.php', loginData)
html = etree.HTML(r.text)

webSensorID = "42"
identifier = "ident"

find = etree.XPath("//table/tr[td[1]/text() = "+ webSensorID +"]/td/text()")

dat = "/home/pi/Running_Programs/"+ identifier +"-" + webSensorID +"Meta.dat"

metaData = [find(html)]
print(dat)
print(metaData)

np.savetxt(dat, metaData, delimiter=',', fmt='%s')

exit
#find43(html)

__all__ = ["GroveSlidePotentiometer"]

pin0 = 0
pin1 = 1
#f=('/home/pi/Running_Programs/currentTest.csv')


class GroveSlidePotentiometer(ADC):
    '''
    Grove Slide Poteniometer Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    
    @property
    def value(self):
        '''
        Get the position value, max position is 100.0%.

        Returns:
            (int): ratio, 0(0.0%) - 1000(100.0%)
        '''
        return self.adc.read(self.channel)


Grove = GroveSlidePotentiometer


def main():
    from grove.helper import SlotHelper
    #sh = SlotHelper(SlotHelper.ADC)
    
    sensor0 = GroveSlidePotentiometer(pin0)
    sensor1 = GroveSlidePotentiometer(pin1)
    i = 0
    start = datetime.datetime.now()
    #unit = "unit"
    
    csv = "/home/pi/Running_Programs/"+ identifier +"-" + webSensorID +".csv"
       
    pinValues = []
    #pinValues.append([])
    pinValues = np.append(pinValues, [str(datetime.datetime.now())])
    #print(pinValues)
    #f=open('/home/pi/Running_Programs/currentTest.dat', 'ab')
    #f='/home/pi/Running_Programs/currentTest.csv'

    while True:
        #when = datetime.datetime.now()
        #pinValues = pinValues[len(pinValues)+1].append([[str(when), sensor0.value, sensor1.value]])
        pinValues = np.append(pinValues, ["0: "+str(sensor0.value), "1: "+str(sensor1.value)])
        #print(pinValues)
        i = i + 1
                
        if i == 7999:
            i = 0
            # print(pinValues)
            pinValues = np.append(pinValues, [str(datetime.datetime.now())])
            with open(csv, "ab") as f:
                np.savetxt(f, pinValues, fmt = "%s")
            #np.savetxt(f, pinValues, delimiter = "     ", fmt="%s")

            pinValues = np.array([])
            exit()
                       
        # time.sleep(.1)    

if __name__ == '__main__':
    main()
