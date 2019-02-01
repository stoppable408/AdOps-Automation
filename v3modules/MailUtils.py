import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from email import encoders
today = date.today().strftime("%A, %B %d, %Y")

def send_message(subject, message, recipients):
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
       smtpObj.sendmail(msg.get('From'), to, msg.as_string())
       print("Successfully sent email")
    except Exception as e:
       print("Error: unable to send email")
       print(e)

       
def send_email(attachmentPath, subject="", message="", recipients=None):

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
       
       for attachment in attachmentPath:
        header = 'attachment; filename="{filename}"'.format(filename=attachment)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', header)
        msg.attach(part)
       smtpObj.sendmail(msg.get('From'), to, msg.as_string())
       print("Successfully sent email")
    except Exception as e:
       print("Error: unable to send email")
       print(e)
       
