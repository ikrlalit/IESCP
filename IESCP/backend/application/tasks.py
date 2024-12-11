from celery import shared_task
import time
from .models import Campaign,AdRequest, InfluencerProfile, User
from flask import current_app
import csv
from .mailer import send_email

import logging

logger = logging.getLogger(__name__)

@shared_task(ignore_result=True)
def add(x,y):
    time.sleep(20)
    print("celery task triggered.")
    return x+y


@shared_task(ignore_result=True)
def export_csv_campaigns():
    with current_app.app_context():
        allcampdata = Campaign.query.with_entities(
            Campaign.name,
            Campaign.description,
            Campaign.budget,
            Campaign.visibility,
            Campaign.start_date,
            Campaign.end_date,
            Campaign.primary_goal
        ).all()

        print(allcampdata)  
        
        output_file = './user-downloads/file.csv'
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Description', 'Budget', 'Visibility', 'Start Date', 'End Date', 'Primary Goal'])
            for row in allcampdata:
                writer.writerow(row)

        print(f"CSV written to {output_file}")
        return output_file

@shared_task(ignore_result=True)
def daily_remainder_mails():
    logger.info("started")
    with current_app.app_context():
        data = AdRequest.query.filter_by(status='Pending').all()
        if data:
            for i in data:
                infdata = InfluencerProfile.query.filter_by(user_id=i.influencer_id).one()
                logger.info(infdata)
                usrdata = User.query.filter_by(id=i.influencer_id).one()
                logger.info(usrdata)
                if infdata and usrdata:
                    logger.info(usrdata.email,infdata.name)
                    send_email(usrdata.email,infdata.name)
    return "OK"

@shared_task(ignore_result=True)
def mothly_remainder_mails():
    send_email()
    return "OK"
