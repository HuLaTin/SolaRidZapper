
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
#The mail addresses and password
sender_address = 'belfordiost@gmail.com'
sender_pass = 'ualri0st'
#receiver_address = 'rebelford@ualr.edu'
receiver_address = 'phwilliams@ualr.edu'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'
#The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
attach_file_name = 'Heifer.jpg'
attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
payload = MIMEBase('application', 'octate-stream')
#payload.set_payload((attach_file).read())
payload.set_payload((attach_file).read())

encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
#payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
#message.attach(attach_file_name,maintype='image')
message.attach(payload)

#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login('belfordiost@gmail.com', 'ualri0st') #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')
