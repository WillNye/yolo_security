from datetime import datetime as dt
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib

from credentials import FROM, SEND_TO, LOGIN_EMAIL, LOGIN_PASSWORD


def send_email():
    msg = MIMEMultipart()
    detection_time = dt.now().strftime("%m/%d/%Y %H:%M:%S")

    # generic email headers
    msg['Subject'] = 'Someone was detected at {}'.format(detection_time)
    msg['From'] = FROM
    msg['To'] = SEND_TO

    # now open the image and attach it to the email
    with open('detected_person.jpg', 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(LOGIN_EMAIL, LOGIN_PASSWORD)
    server.send_message(msg)
    server.close()
