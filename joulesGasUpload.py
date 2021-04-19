#!/usr/bin/env python3


import datetime, time, math, gspread, board, busio, adafruit_bme680
import serial, os, os.path
import RPi.GPIO as GPIO
from gpiozero import MCP3008
from oauth2client.service_account import ServiceAccountCredentials
 
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Running_Programs/joulesData.json', scope) 
#replace mydata.json with the name of your data file
client = gspread.authorize(creds)
sheet = client.open("Joules_Data").sheet1

adc0 = MCP3008(channel=0)
adc1 = MCP3008(channel=1)
adc2 = MCP3008(channel=2)
adc3 = MCP3008(channel=3)
adc4 = MCP3008(channel=4)
adc5 = MCP3008(channel=5)
adc6 = MCP3008(channel=6)
adc7 = MCP3008(channel=7)

i2c = busio.I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

while True:
  when = datetime.datetime.now()
  load = os.popen('uptime | cut -d: -f4 | cut -d, -f1').read()
  throttle = os.popen('vcgencmd get_throttled | cut -d= -f2').read()
  mq2sensorValue = adc0.value
  mq3sensorValue = adc1.value
  mq4sensorValue = adc2.value
  mq5sensorValue = adc3.value
  mq6sensorValue = adc4.value
  mq7sensorValue = adc5.value
  mq8sensorValue = adc6.value
  mq9sensorValue = adc7.value
  load = load.rstrip()
  throttle = throttle.rstrip()
        
  values = [when.strftime('%Y-%m-%d %H:%M:%S.%f'), mq2sensorValue, mq3sensorValue, mq4sensorValue, mq5sensorValue,
            mq6sensorValue,mq7sensorValue, mq8sensorValue, mq9sensorValue, bme680.temperature, bme680.gas,
            bme680.humidity,bme680.pressure, load,throttle]

  inFile = open("/home/pi/Running_Programs/GasStream.csv","a")
  inFile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
                     '' %(when, mq2sensorValue, mq3sensorValue, mq4sensorValue, mq5sensorValue,
                            mq6sensorValue,mq7sensorValue, mq8sensorValue, mq9sensorValue, 
                            bme680.temperature, bme680.gas,
                            bme680.humidity,bme680.pressure,                        
                            load,throttle))    
    
  inFile.close()
        
  try:
      sheet.insert_row(values, 2, value_input_option='RAW')
  except:
      print("Upload failed.")
      client = gspread.authorize(creds)
      sheet = client.open("Joules_Data").sheet1
      sheet.insert_row(values, 2, value_input_option='RAW')
    
  time.sleep(30)
