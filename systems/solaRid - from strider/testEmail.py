#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = "belfordiost@gmail.com"
email_password = "ualri0st"
#email_send = "evlisitsyna@ualr.edu"
email_send = "phwilliams@ualr.edu"

subject = "Test email from pi"

msg = MIMEMultipart()
msg["From"] = email_user
msg["To"] = email_send
msg["Subject"] = subject

body = "Hi there, sending this email from Python!"
msg.attach(MIMEText(body,"plain"))

text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()