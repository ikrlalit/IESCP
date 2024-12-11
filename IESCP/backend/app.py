from flask import Flask, render_template,send_file
from flask_restful import Resource, Api
from flask_cors import CORS 
from application.database import db
from application.config import *
from application.models import *
from flask_jwt_extended import JWTManager
from datetime import timedelta
from application.worker import celery_init_app
from application.tasks import add,export_csv_campaigns,daily_remainder_mails, mothly_remainder_mails
from celery.result import AsyncResult
from flask import jsonify
from celery.schedules import crontab
from application.cache import cache

app=None
api=None

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(LocalConfig)
    db.init_app(app)
    cache.init_app(app)
    jwt = JWTManager(app)
    celery_app = celery_init_app(app)
    
    api=Api(app)
    return app,api,celery_app
app, api,celery_app= create_app()

from application.api import UserAuth, UserSignUp, AdminAPI,SponsorApproval,CampaignAPI,SponsorProfileAPI,GetCampaignListAPI,InfluencersList,AdRequestAPI,GetAdRequestListBySponsorIdAPI, SponsorDashboardSearchAPI,InfluencerDashboardSearchAPI,GetRecommendedCampaigns,InfluencerProfileAPI,GetRecommendedInfluencers,GetAdRequestListByInfluencerIdAPI,InserttoMessages,GetAllMessages,GetInfluecnerDetails,GetPaymentStatus
api.add_resource(UserSignUp, "/api/UserSignUp")
api.add_resource(UserAuth,"/api/UserLogin")
api.add_resource(AdminAPI,"/api/GetAdminDashboardData")
api.add_resource(SponsorApproval,"/api/UpdateSponsorStatus")
api.add_resource(CampaignAPI,"/api/NewCampaign","/api/Campaign/<int:id>")
api.add_resource(GetInfluecnerDetails,"/api/GetInfluecnerDetail/<int:id>")
api.add_resource(AdRequestAPI,"/api/AdRequest","/api/AdRequest/<int:id>")
api.add_resource(InserttoMessages,"/api/AddNewMessage")
api.add_resource(GetCampaignListAPI,"/api/GetCampaignList")
api.add_resource(SponsorDashboardSearchAPI,"/api/SponsorDashboardSearchAPI")
api.add_resource(InfluencerDashboardSearchAPI,"/api/InfluencerDashboardSearchAPI")
api.add_resource(GetAdRequestListBySponsorIdAPI,"/api/GetAdRequestListBySponsorIdAPI")
api.add_resource(GetAdRequestListByInfluencerIdAPI,"/api/GetAdRequestListByInfluencerIdAPI")
api.add_resource(InfluencersList,"/api/GetInfluencersList")
api.add_resource(SponsorProfileAPI,"/api/NewSponsorProfile","/api/NewSponsorProfile/<int:id>")
api.add_resource(InfluencerProfileAPI,"/api/NewInfluencerProfile","/api/NewInfluencerProfile/<int:id>")
api.add_resource(GetRecommendedCampaigns,"/api/GetRecommendedCampaigns")
api.add_resource(GetRecommendedInfluencers,"/api/GetRecommendedInfluencers")
api.add_resource(GetAllMessages,"/api/GetAllMessages")
api.add_resource(GetPaymentStatus,"/api/GetPaymentStatus")

@app.route('/add/<int:x>/<int:y>')
def add_celery(x,y):
    
    task=add.delay(x,y)
    return jsonify({"task_id":task.id})
    
@app.route('/get_data/<task_id>')
def get_data(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        res_obj = {
            'status':result.state,
            'result':result.result,
            'ready':result.ready()
        }
        return jsonify(res_obj),200
    else:
        return "task not ready",405

@app.route('/start-csv-export')
def start_csv_export():
    task=export_csv_campaigns.delay()
    return jsonify({"task_id":task.id})

@app.route('/get-csv-file/<task_id>')
def get_csv_file(task_id):
    try:
        # Directly serve the file
        return send_file('./user-downloads/file.csv'), 200
    except FileNotFoundError:
        return "File not ready", 405

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0, daily_remainder_mails.s(), name='add every 10')

    sender.add_periodic_task(
        crontab(hour=17, minute=30),
        daily_remainder_mails.s(),
        name='daily reminder emails',
    )

    sender.add_periodic_task(
        crontab(hour=8, minute=0, day_of_month=1),  
        monthly_remainder_mails.s(),
        name='monthly reminder emails',
    )


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run( host='0.0.0.0', port=5000)