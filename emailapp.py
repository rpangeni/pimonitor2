import smtplib
import getpass
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import json
import logging


def sendEmailUsingGmail(filename,emailto, msgTxt, gmail_user, gmail_password):
    try:
        logger = logging.getLogger('Emailapp')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        outer = MIMEMultipart()
        outer['Subject'] = 'Movement detected'
        outer['To'] = emailto
        outer['From'] = gmail_user
        outer.attach(MIMEText(msgTxt))
        with open (filename, "rb") as fi1:
            part = MIMEApplication(fi1.read(), Name = basename(filename))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
            outer.attach(part)
        server.sendmail(gmail_user, emailto, outer.as_string())
        logger.info("Sent succesfully.\n")
    except smtplib.SMTPAuthenticationError as e:
        logger.error ("Failed to send email. Probably wrong password\n")
    
if __name__ == '__main__':
    gmail_user = 'rupakpangeni@gmail.com'
    gmail_password = getpass.getpass('enter password for gmail account')
    sendEmailUsingGmail(r'C:/temp/image2016Dec29-201713.jpg', 'r_pangeni@yahoo.com', 'Security image', gmail_user, gmail_password)
