import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time, math, board, busio, serial, datetime, os, csv, adafruit_bme680
from gpiozero import MCP3008
import os.path
import paramiko

#import adafruit_bme680

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

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value pulled low, (6 BCM/ 31 BOARD)

ledCommand = '/home/pi/Running_Programs/LED.py 18 off'
#nameCommand = 'cat /home/pi/Running_Programs/ident.dat'

k = paramiko.RSAKey.from_private_key_file("/home/pi/.ssh/id_rsa")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# !!change to pitunnel!!
c.connect( hostname = "144.167.219.225", username = "pi", pkey = k )

sftp_client = c.open_sftp()

listToFile = []
line = []

#figure out settings for how many readings.
readingsBeforeTrigger = int(10)
readingsAfterTrigger = int(30)
timeTwixtReads = int(1)
maxReads = readingsBeforeTrigger + readingsAfterTrigger

sensorList = ["MQ2", "MQ3", "MQ4", "MQ5", "MQ6", "MQ7", "MQ8", "MQ135", "BME680"]
count = 0
readingCount = 0
eventCheck = 0
errorCounter = 5

eventOn = False
done = False


print("Beginning collection.")
while True:
    eventOn = False
    readingCount = 0
    eventCheck = 0
    count = 0
    listToFile = []
    line = []
    
    today = datetime.date.today()
    outFile = today.strftime("%Y%b%d") + "-"
    outFile = os.path.join("gasRuns", outFile)
    while True:
        count = count + 1

        when = str(datetime.datetime.now())
        chan0 = adc0.value
        chan1 = adc1.value
        chan2 = adc2.value
        chan3 = adc3.value
        chan4 = adc4.value
        chan5 = adc5.value
        chan6 = adc6.value
        chan7 = adc7.value
        line = [when, chan0, chan1, chan2, chan3, chan4, chan5, chan6, chan7, bme680.temperature, bme680.gas, bme680.humidity, bme680.pressure]
         
        listToFile.append(line)
        
        if GPIO.input(6) == GPIO.HIGH:
            eventCheck = eventCheck + 1
            #print("pin high.")
            
        if eventCheck == errorCounter:
          eventOn = True        
          print("Event detected!")
        
        # Issues here
        if GPIO.input(6) == GPIO.LOW and eventCheck > 0 and eventCheck < errorCounter:
          print("False event")
          eventCheck = 0
          eventOn = False
                
        if eventOn == True:
            readingCount = readingCount + 1
        
        if readingCount == (maxReads - readingsBeforeTrigger):
            numrows = len(listToFile)
            subList = listToFile[(numrows - maxReads):][:]
            
            catIdent = sftp_client.open('/home/pi/Running_Programs/ident.dat')
            ident = str(catIdent.readline(6))
            catIdent.close()            
            
            outFile = outFile + "-" + ident +".csv"
            print(outFile)
            
            fileHandle = open(outFile, 'w')
            writer = csv.writer(fileHandle)
            writer.writerows(subList)
            fileHandle.close()
            
            print("done!")                           
            c.exec_command(ledCommand)
            
            while True:
              if GPIO.input(6) == GPIO.HIGH:
                print("LED on, waiting...")
                time.sleep(3)
              else:
                print("Restarting collection...")
                done = True 
                break
        
        if done:
          break

        time.sleep(timeTwixtReads)

