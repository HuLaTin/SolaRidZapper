#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#for send IP
import socket
import fcntl
import struct

email_user = "belfordiost@gmail.com"
email_password = "UALRi0st"
#email_send = "belfordiost@gmail.com"
email_send = "phwilliams@ualr.edu"

#create function to get ip address
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # uncomment the following line if using python2
    #return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])
    # uncomment the following line if using python3
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',bytes(ifname[:15],'utf-8')))[20:24])    

#assign IP address to variable address
#address = get_ip_address('wlan0')

#subject=str(address)

msg = MIMEMultipart()
msg["From"] = email_user
msg["To"] = email_send
#msg["Subject"] = subject
msg["Subject"] = "subject here"

#body="The new IP address of Solarid Unit 2 is " + str(address)
body="The new IP address of Solarid Unit 2 is "

msg.attach(MIMEText(body,"plain"))
text = msg.as_string()

#attach_file_name = 'Heifer.jpg'
attach_file_name = 'params,30000,8000,testOutFilename.csv'
attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
payload = MIMEBase('application', 'octate-stream')
#payload.set_payload((attach_file).read())
payload.set_payload((attach_file).read())

encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
#payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
#message.attach(attach_file_name,maintype='image')
msg.attach(payload)

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()
