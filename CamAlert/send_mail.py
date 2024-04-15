import imghdr
import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


def send_email(image_path):
    print('e1')
    email_msg = EmailMessage()
    email_msg['Subject'] = 'New alert'
    email_msg.set_content('Here is a new intruder!')

    with open(image_path, 'rb') as file:
        content = file.read()
    email_msg.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    host = 'smtp.gmail.com'
    port = 587

    login = os.getenv('MAIL_USER')
    pw = os.getenv('MAIL_PW')
    receiver = 'prowlersk8@gmail.com'

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(login, pw)
    gmail.sendmail(login, receiver, email_msg.as_string())
    gmail.quit()
    print('e2')
