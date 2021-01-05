#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import saia
import smtplib,ssl
from socket import gaierror
import configparser
import os
import email.utils
from email.mime.text import MIMEText

basePath = os.environ.get('PIHEIZ')
basePath= basePath if basePath is not None else os.getcwd() 

config = configparser.ConfigParser()
config.read(os.path.join(basePath, 'config.ini'))

port = int(config.get('EMAILSETTINGS','port'))
smtp_server = config.get('EMAILSETTINGS','smtp_server')
login = config.get('EMAILSETTINGS','login')
password = config.get('EMAILSETTINGS','password')

# specify the sender’s and receiver’s email addresses
sender = config.get('EMAILSETTINGS','sender')
receiver = [e.strip() for e in config.get('EMAILSETTINGS', 'receiver').split(',')] 


def send_email(title,value):
 
    msg = MIMEText(f'{title} --> {value}')
    msg['To'] = ", ".join(receiver)
    msg['From'] = email.utils.formataddr(('Alarm Heizung', 'alarm@heizung.com'))
    msg['Subject'] = title

    try:
        context = ssl.create_default_context()

        #send your message with credentials specified above
        with smtplib.SMTP_SSL(smtp_server, port,context=context) as server:
            server.login(login, password)
            server.sendmail(sender, receiver, msg.as_string())

        # tell the script to report if your message was sent or which errors need to be fixed 
        print('Sent')
    except (gaierror, ConnectionRefusedError):
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))

def check_error_flag():
    lastvalue=config.get('ALARMINGSTORE','Alarm_IO', fallback='1')
    error= saia.get_value(config['READVALUES']['Kas.WP1.Schalter_Alarm_IO'])
    error='0'
    if (int(error)==0 and  int(lastvalue)==1):
        send_email("Heizung WP1 hat ein Fehler", error)

    if (int(error)==1 and  int(lastvalue)==0):
        send_email("Heizung WP1 hat KEINEN Fehler mehr", error)
    if (not config.has_section('ALARMINGSTORE')):
        config.add_section('ALARMINGSTORE')
    config.set('ALARMINGSTORE','Alarm_IO',error)
    with open(os.path.join(basePath, 'config.ini'), 'w') as conf:
        config.write(conf)


check_error_flag()