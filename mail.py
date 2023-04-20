from zipfile import ZipFile
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import argparse
import re

# adding arguments 
parser = argparse.ArgumentParser(description="zip-mail python")
parser.add_argument("-c", dest="config", default='conf.json', type=str)
args = parser.parse_args()

#calling variables
f = open (args.config)                    
data = json.load(f)
folder=data['folder']   
outFileName=data['outFileName']   
inFileName=data['inFileName']    
Server=data['Server']
Port=data['Port']
User=data['User']
Passwd=data['Passwd']
Subject=data['Subject']
From=data['From']  
To=data['To']  
Text=data['Text']  

#variable for email check
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

#email check
def isValid(email):
    if re.fullmatch(regex, email):
      pass
    else:
      print("Invalid email" + ' ' + email)
      exit()   

#zip folder or file
def zipFolder(dirName, zipFileName, filterFile):
    with ZipFile(zipFileName, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                if filterFile(filename):
                    filepath = os.path.join(folderName, filename)
                    zipObj.write(filepath)

#send email with zip
def sendEmail():
    msg = MIMEMultipart()
    msg_text = MIMEText(Text, 'plain')
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To
    msg.attach(msg_text)
    with open(outFileName,'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name = outFileName))
    with smtplib.SMTP_SSL(Server, Port) as smtp_obj:
        smtp_obj.login(User, Passwd)
        smtp_obj.sendmail(msg['From'], msg["To"].split(","), msg.as_string())
        smtp_obj.quit()

#check recepient    
isValid(To)
#check sender
isValid(From)
#zip foder
zipFolder(folder, outFileName, lambda name : inFileName in name)
#send email
sendEmail()

