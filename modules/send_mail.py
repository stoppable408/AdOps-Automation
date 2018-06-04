import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from email import encoders
today = date.today().strftime("%A, %B %d, %Y")

def send_email(attachmentPath, elapsedTime = None, title=None, recipients=None):
    global today    
    
    if elapsedTime != None:
        header = 'attachment; filename="LMA Report for {0}.xlsx"'.format(today)
        subject = "Full LMA Report for " + today
        message = "Attached is the Full LMA report for today: {0}...This report took {1} to run today.".format(today, elapsedTime)
    else:
        header = 'attachment; filename="{0} Update Report for {1}.xlsx"'.format(title,today)
        subject = "Updated {0} for {1}".format(title,today)
        message = "Attached is an excel file containing all of the {0} that were updated today.".format(title)
        
    to = recipients
    email = "Reporting@dentsuaegis.com"
    try:
       smtpObj = smtplib.SMTP('internalsmtprelay.media.global.loc')
       msg = MIMEMultipart()
       msg['Subject'] = subject
       msg['From'] = email
       msg['To'] = ", ".join(to)
       body = MIMEText(message,'html')
       msg.attach(body)
       
       part = MIMEBase('application', "octet-stream")
       part.set_payload(open(attachmentPath, "rb").read())
       encoders.encode_base64(part)
       
       part.add_header('Content-Disposition', header)
       msg.attach(part)
       smtpObj.sendmail(msg.get('From'), to, msg.as_string())
       print("Successfully sent email")
    except Exception as e:
       print("Error: unable to send email")
       print(e)
       
