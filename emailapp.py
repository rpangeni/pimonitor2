import smtplib
import getpass
import sys
import imaplib
import email
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
        server.logout()
    except smtplib.SMTPAuthenticationError as e:
        logger.error ("Failed to send email. Probably wrong password\n")


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def checkEmail(mail_user, mail_secret):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(mail_user, mail_secret)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.
    result, data = mail.uid('search', None, "ALL")  # search and return uids instead
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email.decode("utf-8"))
    print(email_message['To'])
    print(email.utils.parseaddr(email_message['From']) ) # for parsing "Yuji Tomita" <yuji@grovemade.com>
    print(email_message.items())  # print all headers
    print(get_first_text_block(email_message))


if __name__ == '__main__':
    gmail_user = 'rupakpangeni@gmail.com'
    gmail_password = getpass.getpass('enter password for gmail account')
    checkEmail('rupakpangeni@gmail.com', gmail_password)
    #sendEmailUsingGmail(r'C:/temp/image2016Dec29-201713.jpg', 'r_pangeni@yahoo.com', 'Security image', gmail_user, gmail_password)
