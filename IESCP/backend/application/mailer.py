import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template,current_app

def send_email(sendto,infname):

    SMTP_SERVER = 'localhost'
    SMTP_PORT = 1025
    SENDER_EMAIL = 'dontreply@iescp-mailer.com'
    SENDER_PASSWORD = ''
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = sendto
    msg['Subject'] = 'Ad Request Pending'
    
    with current_app.app_context():
        body = render_template('dailyremainder.html', influencer_name=infname)
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_monthly_email(sendto,infname):

    SMTP_SERVER = 'localhost'
    SMTP_PORT = 1025
    SENDER_EMAIL = 'dontreply@iescp-mailer.com'
    SENDER_PASSWORD = ''
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = sendto
    msg['Subject'] = 'Monthly Report'
    
    with current_app.app_context():
        body = render_template('monthlyremainder.html',data)
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()