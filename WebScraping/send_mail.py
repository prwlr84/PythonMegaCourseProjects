import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(text):
    host = 'smtp.gmail.com'
    port = 465

    login = os.getenv('MAIL_USER')
    pw = os.getenv('MAIL_PW')

    context = ssl.create_default_context()
    receiver = 'prowlersk8@gmail.com'

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(login, pw)
        server.sendmail(login, receiver, text)
