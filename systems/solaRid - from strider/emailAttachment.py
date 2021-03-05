#!/usr/bin/python

import sys

if (len(sys.argv) - 1) < 2:
  print("Need command line arguments, example;")
  print("./scriptName emailID filenameToSend")
  print(sys.argv[0] + " belfordiost@gmail.com params,30000,8000,testOutFilename.csv")
  print(sys.argv[0] + " phwilliams@ualr.edu params,30000,8000,testOutFilename.csv")
  exit(1)

emailID = sys.argv[1]
filename = sys.argv[2]

import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

FILENAME = os.path.basename(filename)
#print "FILENAME" , FILENAME

SUBJECT = 'Subject string'
FILEPATH = filename
#FILENAME = 'params,30000,8000,testOutFilename.csv'
MY_EMAIL = 'belfordiost@gmail.com'
MY_PASSWORD = 'UALRi0st'
#TO_EMAIL = 'phwilliams@ualr.edu'
TO_EMAIL = emailID
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = COMMASPACE.join([TO_EMAIL])
msg['Subject'] = FILENAME

part = MIMEBase('application', "octet-stream")
part.set_payload(open(FILEPATH, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
# part.add_header('Content-Disposition', 'attachment; filename="attachthisfile.csv"')

msg.attach(part)

smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(MY_EMAIL, MY_PASSWORD)
smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
smtpObj.quit()

