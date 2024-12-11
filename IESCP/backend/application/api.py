
import datetime
from flask_restful import Resource,fields, marshal_with, reqparse, request, Resource
from application.models import User,SponsorProfile,InfluencerProfile,Campaign,AdRequest,Messages,Payments
from application.validation import *
from application.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token,get_jwt_identity, jwt_required
import os
from application.config import *
from sqlalchemy import desc
from flask import jsonify
from .cache import cache

#################### Admin, Sponsor, Infulencer Registration APIs ################

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("email", required=True)
create_user_parser.add_argument("username", required=True)
create_user_parser.add_argument("password", required=True)
create_user_parser.add_argument("role", required=True)

create_user_parser.add_argument("companyname")
create_user_parser.add_argument("industry")
create_user_parser.add_argument("budget")
create_user_parser.add_argument("contactemail")
create_user_parser.add_argument("websitelink")

create_user_parser.add_argument("influencername")
create_user_parser.add_argument("category")
create_user_parser.add_argument("niche")
create_user_parser.add_argument("youtube_follower")
create_user_parser.add_argument("youtube_link")
create_user_parser.add_argument("instagram_follower")
create_user_parser.add_argument("instagram_link")
create_user_parser.add_argument("twitter_follower")
create_user_parser.add_argument("twitter_link")
                
class UserSignUp(Resource):
    def post(self):
        try:
            args = create_user_parser.parse_args()
            username = args.get('username')

            if User.query.filter_by(username=username).first():
                raise BusinessValidationError(400, "UBE001", 'Username already exists.')
            email = args.get('email')
            
            if User.query.filter_by(email=email).first():
                raise BusinessValidationError(400, "UBE002", 'Email already exists.')
        
            password = args.get('password')
            role = args.get('role')

            if not username:
                raise BusinessValidationError(400, "UBE003", "Username is required")
            if not email:
                raise BusinessValidationError(400, "UBE003", "Email is required")
            if not password:
                raise BusinessValidationError(400, "UBE004", 'Password is required')
 
            status = "pending" if role == "sponsor" else "approved"

            new_user = User(username=username, email=email, password=generate_password_hash(password), role=role, status=status)
            db.session.add(new_user)
            db.session.commit()
            
            ########### Create Sponsor Profile / Influencer profile #############
            if role =="sponsor":
                companyname = args.get('companyname')
                industry = args.get("industry")
                budget = args.get("budget")
                contactemail = args.get("contactemail")
                websitelink = args.get("websitelink")
                user_id= new_user.id

                sponsor_profile= SponsorProfile(name=companyname, industry=industry,budget=budget,contact_email=contactemail, website_link=websitelink,user_id=user_id)
                db.session.add(sponsor_profile)
                db.session.commit()


            if role =="influencer":
                name = args.get('influencername')
                category = args.get("category")
                niche = args.get("niche")
                youtube_follower = args.get("youtube_follower")
                youtube_link = args.get("youtube_link")
                instagram_follower = args.get("instagram_follower")
                instagram_link = args.get("instagram_link")
                twitter_follower = args.get("twitter_follower")
                twitter_link = args.get("twitter_link")
                user_id= new_user.id

                influencer_profile = InfluencerProfile(name=name,category=category,niche=niche,youtube_follower=youtube_follower,youtube_link=youtube_link,instagram_follower=instagram_follower,instagram_link=instagram_link,twitter_follower=twitter_follower,twitter_link=twitter_link,user_id=user_id)
                db.session.add(influencer_profile)
                db.session.commit()

            json_response = {
                "status_code":200,
                "data": new_user.to_dict(),
                "message": "User created successfully",
            }
            return jsonify(json_response)
        
        except BusinessValidationError as e:
            db.session.rollback()
            json_response = {
                "status_code": e.status_code,
                "data": {},
                "message": e.error_message}
            return jsonify(json_response)

        except Exception as e:
            db.session.rollback()
            json_response = {
                "status_code":500,
                "data": {},
                "message": str(e)}
            return jsonify(json_response)
   
############################ User Authentication APIs #################################

create_userauth_parser=reqparse.RequestParser()
create_userauth_parser.add_argument("email", required=True)
create_userauth_parser.add_argument("password", required=True)

class UserAuth(Resource):
    def post(self):
        args = create_userauth_parser.parse_args()
        email = args.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            password = args.get('password')
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity={'email': user.email, 'id': user.id})
                json_response ={
                "status_code":200,
                "data": {'access_token': access_token, 'email': email, 'role': user.role,'status':user.status},
                "message": "Login Successful."
                }
                return jsonify(json_response)
            else:
                json_response ={
                "status_code":400,
                "data": {},
                "message": "Invalid credentials."
                }
                return jsonify(json_response)
        else:
            json_response ={
                "status_code":404,
                "data": {},
                "message": "User not found."
                }
            return jsonify(json_response)
        
#################### Sponsor Approval API ###########################

sponsor_status_update_parser = reqparse.RequestParser()
sponsor_status_update_parser.add_argument('sponsorUserId', type=int, required=True, help='sponsorUserId is required')
sponsor_status_update_parser.add_argument('isApproved', type=int, required=True, help='isApproved is required')

class SponsorApproval(Resource):
    def put(self):
        args = sponsor_status_update_parser.parse_args()
            
        sponsor_user_id = args.get('sponsorUserId')
        is_approved = args.get('isApproved')

        user = User.query.filter_by(id=sponsor_user_id).first()
        
        if user:
            if is_approved == 1:
                user.status = 'approved'
                db.session.commit()
                return jsonify({"message": "User account approved", "status": 200})
            elif is_approved == 0:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"message": "User account rejected and deleted", "status": 200})
            else:
                return jsonify({"message": "Invalid value for isApproved", "status": 400})
        else:
            return jsonify({"message": "No user found", "status": 404})
        

########################## SponsorProfile CRUD APIs #######################

sponsor_profile_fields={
    "name": fields.String,
    "industry":fields.String,
    "budget":fields.Float,
    "user_id":fields.Integer,
}


create_sponsorprofile_parser = reqparse.RequestParser()
create_sponsorprofile_parser.add_argument('name', type=str, required=True, help='Sponsor name is required')
create_sponsorprofile_parser.add_argument('industry', type=str, required=True, help='Industry name is required')
create_sponsorprofile_parser.add_argument('budget', type=str, required=True, help='Budget is required')

update_sponsorprofile_parser = reqparse.RequestParser()
update_sponsorprofile_parser.add_argument('companyname', type=str)
update_sponsorprofile_parser.add_argument('industry', type=str)
update_sponsorprofile_parser.add_argument('budget')
update_sponsorprofile_parser.add_argument('contactemail', type=str)
update_sponsorprofile_parser.add_argument('websitelink', type=str)


class SponsorProfileAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            sponsor = get_jwt_identity()
            user_id = sponsor['id']
            args = create_sponsorprofile_parser.parse_args()
            
            name = args.get('name')
            industry = args.get('industry')
            budget = args.get('budget')

            if not name:
                raise BusinessValidationError(400, "SBE001", "Individual/Compnay name is required.")
            if not industry:
                raise BusinessValidationError(400, "SBE002", "Industry name is required.")
            if not budget:
                raise BusinessValidationError(400, "SBE003", "Budget is required.")
            if not user_id:
                raise BusinessValidationError(400, "SBE004", "User_id is required.")

            new_sponsor_profile = SponsorProfile(name=name, industry=industry, budget=budget,user_id=user_id)
            db.session.add(new_sponsor_profile)
            db.session.commit()
            return 201

        except BusinessValidationError as bve:
            return {"error": {"status_code": bve.status_code, "error_code": bve.error_code, "error_message": bve.error_message}}, bve.status_code

        except Exception as e:
            db.session.rollback()  
            return {"error": str(e)}, 500
        finally:
            db.session.close()

    @jwt_required()
    def get(self):
        sponsor = get_jwt_identity()
        user_id = sponsor['id']
        try:
            sponsorprofile=SponsorProfile.query.filter_by(user_id=user_id).first()
            # print(sponsorprofile.to_dict())

            if sponsorprofile:
                userdata = User.query.filter_by(id=user_id).first()
                sponsorprofiledict=sponsorprofile.to_dict()
                userdatadict = userdata.to_dict()
                sponsorprofiledict['username'] = userdatadict['username']
                sponsorprofiledict['email'] = userdatadict['email']
                sponsorprofiledict['role'] = userdatadict['role']
                sponsorprofiledict['status'] = userdatadict['status']
            
                if sponsorprofiledict:
                    json_response = {
                        "status_code": 200,
                        "data": sponsorprofiledict,
                        "message": "Data fetched."
                    }
                    return jsonify(json_response)
                else:
                    json_response = {
                        "status_code": 200,
                        "data": {},
                        "message": "Data not fetched."
                    }
                    return jsonify(json_response)
            else:
                json_response = {
                        "status_code": 404,
                        "data": {},
                        "message": "Data not fetched."
                    }
                return jsonify(json_response)
            
        except Exception as e:
            print(str(e))
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
    
    
    @jwt_required()
    def put(self,id):

        sponsor = get_jwt_identity()
        user_id = sponsor['id']
        sponsorprofile=SponsorProfile.query.filter_by(id=id).first()
        if sponsorprofile:
            try:    

                args = update_sponsorprofile_parser.parse_args()
                name = args.get('companyname')
                industry = args.get('industry')
                budget = args.get('budget')
                contactemail = args.get('contactemail')
                websitelink = args.get('websitelink')

                sponsorprofile.name = name if name else sponsorprofile.name
                sponsorprofile.industry = industry if industry else sponsorprofile.industry
                sponsorprofile.budget = budget if budget else sponsorprofile.budget
                sponsorprofile.contactemail = contactemail if contactemail else sponsorprofile.contactemail
                sponsorprofile.websitelink = websitelink if websitelink else sponsorprofile.websitelink

                db.session.commit()
                return 200
            except Exception as e:
                return {"error":str(e)},500
        else:
            raise NotFoundError(status_code=404)
        
    def delete(self,id):
        sponsorprofile =SponsorProfile.query.filter_by(id=id).first()
        db.session.delete(sponsorprofile)
        db.session.commit()
        return 200
    
########################## InfluencerProfile CRUD APIs #######################

update_influencerprofile_parser = reqparse.RequestParser()
update_influencerprofile_parser.add_argument('name', type=str)
update_influencerprofile_parser.add_argument('category', type=str)
update_influencerprofile_parser.add_argument('niche', type=str)
update_influencerprofile_parser.add_argument('instagram_link', type=str)
update_influencerprofile_parser.add_argument('instagram_follower', type=str)
update_influencerprofile_parser.add_argument('twitter_link', type=str)
update_influencerprofile_parser.add_argument('twitter_follower', type=str)
update_influencerprofile_parser.add_argument('youtube_link', type=str)
update_influencerprofile_parser.add_argument('youtube_follower', type=str)


class InfluencerProfileAPI(Resource):
    def post(self):
        try:
            name = request.form.get('name', '').strip()
            category = request.form.get('category', '').strip()
            niche = request.form.get('niche', '').strip()
            reach = request.form.get('category', '').strip()
            user_id = request.form.get('user_id')

            if not name:
                raise BusinessValidationError(400, "IBE001", "Infuencer name is required.")
            if not category:
                raise BusinessValidationError(400, "IBE002", "Category is required.")
            if not niche:
                raise BusinessValidationError(400, "IBE003", "Niche is required.")
            if not reach:
                raise BusinessValidationError(400, "IBE004", "Reach is required.")
            if not user_id:
                raise BusinessValidationError(400, "IBE005", "User_id is required.")

            new_influencer = InfluencerProfile(name=name, category=category, niche=niche,reach=reach,user_id=user_id)
            db.session.add(new_influencer)
            db.session.commit()
            return 201

        except BusinessValidationError as bve:
            return {"error": {"status_code": bve.status_code, "error_code": bve.error_code, "error_message": bve.error_message}}, bve.status_code

        except Exception as e:
            db.session.rollback()  
            return {"error": str(e)}, 500
        finally:
            db.session.close()

    @jwt_required()
    @cache.cached(timeout=50)
    def get(self):
        try:
            inf = get_jwt_identity()
            user_id = inf['id']
            influencerprofile=InfluencerProfile.query.filter_by(user_id=user_id).first()
            if influencerprofile:
                userdata = User.query.filter_by(id=user_id).first()
                influencerprofiledict=influencerprofile.to_dict()
                userdatadict = userdata.to_dict()
                influencerprofiledict['username'] = userdatadict['username']
                influencerprofiledict['email'] = userdatadict['email']
                influencerprofiledict['role'] = userdatadict['role']
                influencerprofiledict['status'] = userdatadict['status']
                if influencerprofiledict:
                    json_response = {
                        "status_code": 200,
                        "data": influencerprofiledict,
                        "message": "Data fetched."
                    }
                    return jsonify(json_response)
                else:
                    json_response = {
                        "status_code": 200,
                        "data": {},
                        "message": "Data not fetched."
                    }
                    return jsonify(json_response)
            else:
                json_response = {
                        "status_code": 404,
                        "data": {},
                        "message": "Data not fetched."
                    }
                return jsonify(json_response)
            
        except Exception as e:
            print(str(e))
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
    
    def put(self,id):
        influencer_profile = InfluencerProfile.query.filter_by(id=id).first()
        if not influencer_profile:
            raise NotFound(description="Influencer profile not found")

        try:
            args = update_influencerprofile_parser.parse_args()

            influencer_profile.name = args['name'] or influencer_profile.name
            influencer_profile.category = args['category'] or influencer_profile.category
            influencer_profile.niche = args['niche'] or influencer_profile.niche
            influencer_profile.instagram_link = args['instagram_link'] or influencer_profile.instagram_link
            influencer_profile.instagram_follower = args['instagram_follower'] or influencer_profile.instagram_follower
            influencer_profile.twitter_link = args['twitter_link'] or influencer_profile.twitter_link
            influencer_profile.twitter_follower = args['twitter_follower'] or influencer_profile.twitter_follower
            influencer_profile.youtube_link = args['youtube_link'] or influencer_profile.youtube_link
            influencer_profile.youtube_follower = args['youtube_follower'] or influencer_profile.youtube_follower

            db.session.commit()

            return {"message": "Profile updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class GetInfluecnerDetails(Resource):
    @jwt_required()
    def get(self,id):
        try:
            inf = get_jwt_identity()
            user_id = inf['id']
            influencerprofile=InfluencerProfile.query.filter_by(user_id=id).first()
            if influencerprofile:
                userdata = User.query.filter_by(id=id).first()
                influencerprofiledict=influencerprofile.to_dict()
                userdatadict = userdata.to_dict()
                influencerprofiledict['username'] = userdatadict['username']
                influencerprofiledict['email'] = userdatadict['email']
                influencerprofiledict['role'] = userdatadict['role']
                influencerprofiledict['status'] = userdatadict['status']
                if influencerprofiledict:
                    json_response = {
                        "status_code": 200,
                        "data": influencerprofiledict,
                        "message": "Data fetched."
                    }
                    return jsonify(json_response)
                else:
                    json_response = {
                        "status_code": 200,
                        "data": {},
                        "message": "Data not fetched."
                    }
                    return jsonify(json_response)
            else:
                json_response = {
                        "status_code": 404,
                        "data": {},
                        "message": "Data not fetched."
                    }
                return jsonify(json_response)
            
        except Exception as e:
            print(str(e))
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

search_reqparser = reqparse.RequestParser()
search_reqparser.add_argument('SearchTerm', type=str)
    
class InfluencersList(Resource):
    def post(self):
        try:
            args = search_reqparser.parse_args()
            search_term = args.get('SearchTerm')
            
            if search_term:
                influencers = InfluencerProfile.query.filter(InfluencerProfile.name.like(f'{search_term}%')).all()
            else:
                influencers = InfluencerProfile.query.all()
            influencers_list = [influencer.to_dict() for influencer in influencers]
            if influencers_list:
                json_response = {
                    "status_code": 200,
                    "data": influencers_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
        
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

class GetRecommendedInfluencers(Resource):
    @jwt_required()
    def get(self):
        try:
            inf = get_jwt_identity()
            user_id = inf['id']
            sp=SponsorProfile.query.filter_by(user_id=user_id).first()
            industry = sp.industry
            print(industry)
            InfluencerProfiles = InfluencerProfile.query.filter(InfluencerProfile.category.like(f'%{industry}%')).all()
            inflist =[]
            if InfluencerProfiles:
                inflist = [i.to_dict() for i in InfluencerProfiles]

                # userdata = User.query.filter_by(id=user_id).first()
                # influencerprofiledict=influencerprofile.to_dict()
                # userdatadict = userdata.to_dict()
                # influencerprofiledict['username'] = userdatadict['username']
                # influencerprofiledict['email'] = userdatadict['email']
                # influencerprofiledict['role'] = userdatadict['role']
                # influencerprofiledict['status'] = userdatadict['status']
                if inflist:
                    json_response = {
                        "status_code": 200,
                        "data": inflist,
                        "message": "Data fetched."
                    }
                    return jsonify(json_response)
                else:
                    json_response = {
                        "status_code": 200,
                        "data": {},
                        "message": "Data not fetched."
                    }
                    return jsonify(json_response)
            else:
                json_response = {
                        "status_code": 404,
                        "data": {},
                        "message": "Data not fetched."
                    }
                return jsonify(json_response)
            
        except Exception as e:
            print(str(e))
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
    

########################## Campaign CRUD APIs #######################

create_campaign_parser = reqparse.RequestParser()
create_campaign_parser.add_argument('name', type=str, required=True, help='Campaign name is required')
create_campaign_parser.add_argument('description', type=str, required=True, help='Description is required')
create_campaign_parser.add_argument('start_date', type=str, required=True, help='Start Date is required')
create_campaign_parser.add_argument('end_date', type=str, required=True, help='End Date is required')
create_campaign_parser.add_argument('budget', type=float, required=True, help='Budget is required')
create_campaign_parser.add_argument('visibility', type=str, required=True, help='Visibility is required')
create_campaign_parser.add_argument('primary_goal', type=str)
create_campaign_parser.add_argument('secondary_goal', type=str)

update_campaign_parser = reqparse.RequestParser()
update_campaign_parser.add_argument('name', type=str)
update_campaign_parser.add_argument('description')
update_campaign_parser.add_argument('start_date')
update_campaign_parser.add_argument('end_date')
update_campaign_parser.add_argument('budget')
update_campaign_parser.add_argument('visibility')
update_campaign_parser.add_argument('primary_goal', type=str)
update_campaign_parser.add_argument('secondary_goal', type=str)

class CampaignAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            sponsor = get_jwt_identity()
            sponsor_id = sponsor['id']
            args = create_campaign_parser.parse_args()
            name = args['name']
            description = args['description']
            start_date = args['start_date']
            end_date = args['end_date']
            budget = args['budget']
            visibility = args['visibility']
            primary_goal = args['primary_goal']
            secondary_goal = args['secondary_goal']

            if not name:
                raise BusinessValidationError(400, "CBE001", "Campaign name is required.")
            if not description:
                raise BusinessValidationError(400, "CBE002", "Description is required.")
            if not start_date:
                raise BusinessValidationError(400, "CBE003", "Start Date is required.")
            if not end_date:
                raise BusinessValidationError(400, "CBE004", "End Date is required.")
            if not budget:
                raise BusinessValidationError(400, "CBE005", "Budget is required.")
            if not primary_goal:
                raise BusinessValidationError(400, "CBE006", "Primary Goal is required.")
            if not visibility:
                raise BusinessValidationError(400, "CBE007", "Visibility is required.")

            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

            new_campaign = Campaign(
                name=name,
                description=description,
                start_date=start_date_obj,
                end_date=end_date_obj,
                budget=budget,
                primary_goal=primary_goal,
                secondary_goal=secondary_goal,
                visibility=visibility,
                sponsor_id=sponsor_id,
                is_inappropriate = 0
            )

            db.session.add(new_campaign)
            db.session.commit()

            json_response = {
                "status_code":200,
                "data": new_campaign.to_dict(),
                "message": "Campaign created successfully",
            }
            return jsonify(json_response)
        
        except BusinessValidationError as e:
            db.session.rollback()
            json_response = {
                "status_code": e.status_code,
                "data": {},
                "message": e.error_message}
            return jsonify(json_response)

        except Exception as e:
            db.session.rollback()
            json_response = {
                "status_code":500,
                "data": {},
                "message": str(e)}
            return jsonify(json_response)


    def get(self,id):
        try:
            campaign = Campaign.query.filter_by(id=id).first()
            if campaign:
                json_response = {
                    "status_code": 200,
                    "data": campaign.to_dict(),
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": {},
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
        
    @jwt_required()
    def put(self, id):
        campaign = Campaign.query.filter_by(id=id).first()
        if campaign:
            try:
                sponsor = get_jwt_identity()
                sponsor_id = sponsor['id']
                args = request.get_json()

                name = args.get('name')
                description = args.get('description')
                start_date = args.get('start_date')
                end_date = args.get('end_date')
                budget = args.get('budget')
                visibility = args.get('visibility')
                primary_goal = args.get('primary_goal')
                secondary_goal = args.get('secondary_goal')
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

                if campaign.sponsor_id == sponsor_id:

                    campaign.name = name if name else campaign.name
                    campaign.description = description if description else campaign.description
                    campaign.start_date = start_date_obj if start_date else campaign.start_date
                    campaign.end_date = end_date_obj if end_date else campaign.end_date
                    campaign.budget = budget if budget else campaign.budget
                    campaign.visibility = visibility if visibility else campaign.visibility
                    campaign.primary_goal = primary_goal if primary_goal else campaign.primary_goal
                    campaign.secondary_goal = secondary_goal if secondary_goal else campaign.secondary_goal

                    db.session.commit()
                    json_response = {
                        "status_code": 200,
                        "message": "Campaign updated successfully.",
                    }
                    return jsonify(json_response)
                else:
                    return jsonify({
                        "status_code": 403,
                        "message": "You are not authorized to update this campaign."
                    }), 403
            except Exception as e:
                db.session.rollback()
                json_response = {
                    "status_code": 500,
                    "message": str(e)
                }
                return jsonify(json_response)
        else:
            return jsonify({
                "status_code": 404,
                "message": "Campaign not found."
            })
        
    def delete(self,id):
        try:
            campaign=Campaign.query.filter_by(id=id).first()
            if campaign:
                db.session.delete(campaign)
                db.session.commit()

                json_response = {
                    "status_code": 200,
                    "message": "Campaign deleted."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 404,
                    "message": "Campaign not found."
                }
                return jsonify(json_response)
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

class GetCampaignListAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            sponsorid = get_jwt_identity()
            spid = sponsorid['id']
            print("dddddddddddd")
            print(spid)
            campaigns = Campaign.query.filter_by(sponsor_id=spid).order_by(Campaign.id.desc()).all()
            campaigns_list = [campaign.to_dict() for campaign in campaigns]
            if campaigns_list:
                json_response = {
                    "status_code": 200,
                    "data": campaigns_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

class GetRecommendedCampaigns(Resource):
    @jwt_required()
    def get(self):
        try:    
            infid = get_jwt_identity()
            inf_id = infid['id']
            print(inf_id,"inf id")
            inf = InfluencerProfile.query.filter_by(user_id = inf_id).first()
            recommended_campaigns_list=[]
            print(inf)
            if inf:
                cate = inf.category
                niche = inf.niche
                sponsordata = SponsorProfile.query.filter(SponsorProfile.industry.like(f"%{cate}%")).all()
                sponsorids = [i.user_id for i in sponsordata] if sponsordata else []
                if sponsorids:
                    recommededcampdata = Campaign.query.filter(Campaign.sponsor_id.in_(sponsorids)).all()
                    recommended_campaigns_list = [i.to_dict() for i in recommededcampdata]

            if recommended_campaigns_list:
                json_response = {
                    "status_code": 200,
                    "data": recommended_campaigns_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
        
########################## AdRequest CRUD APIs #######################

create_adrequest_parser = reqparse.RequestParser()
create_adrequest_parser.add_argument('campaign_id', type=str, required=True, help='Campaign Id is required')
create_adrequest_parser.add_argument('influencer_id', type=str, required=True, help='influencer id is required')
create_adrequest_parser.add_argument('requirements', type=str, required=True, help='Please enter requirements')
create_adrequest_parser.add_argument('payment_amount', type=int, required=True, help='Payment amount is required')

update_adrequest_parser = reqparse.RequestParser()
update_adrequest_parser.add_argument('campaign_id')
update_adrequest_parser.add_argument('influencer_id')
update_adrequest_parser.add_argument('requirements')
update_adrequest_parser.add_argument('payment_amount')
update_adrequest_parser.add_argument('status')


class AdRequestAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            user = get_jwt_identity()
            sponsor_id = user['id']
            args = create_adrequest_parser.parse_args()
            campaign_id = args.get('campaign_id')
            influencer_id = args.get('influencer_id')
            requirements = args.get('requirements')
            payment_amount = args.get('payment_amount')
            new_adrequest = AdRequest(campaign_id=campaign_id,influencer_id=influencer_id,sponsor_id=sponsor_id, requirements=requirements,payment_amount=payment_amount)
            db.session.add(new_adrequest)
            db.session.commit()

            if new_adrequest:
                json_response = {
                    "status_code":200,
                    "data": new_adrequest.to_dict(),
                    "message": "Adrequest created successfully",
                }
                return jsonify(json_response)
            else:
                json_response = {   
                    "status_code":400,
                    "data": {},
                    "message": "Adrequest not created.",
                }
                return jsonify(json_response)

        except Exception as e:
            db.session.rollback()
            json_response = {
                "status_code":500,
                "data": {},
                "message": str(e)}
            return jsonify(json_response)

    def get(self,id):
        try:
            adrequest=AdRequest.query.filter_by(id=id).first()
            campid = adrequest.campaign_id
            campaign = Campaign.query.filter_by(id = campid).first()
            spid = adrequest.sponsor_id
            spnosor = SponsorProfile.query.filter_by( user_id = spid).first()
            infid = adrequest.influencer_id
            influencer = InfluencerProfile.query.filter_by( id = infid).first()
            adrequest_dict = adrequest.to_dict()
            adrequest_dict['campaign_name'] = campaign.name
            adrequest_dict['sponsor_name'] = spnosor.name
            adrequest_dict['influencer_name'] = influencer.name
            if adrequest_dict:
                json_response = {
                    "status_code": 200,
                    "data": adrequest_dict,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": {},
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)
    
    def put(self,id):
        adrequest=AdRequest.query.filter_by(id=id).first()
        print(111111111111111)
        if adrequest:
            try:
                print(adrequest.to_dict())
                print(222222222222222)
                args = update_adrequest_parser.parse_args()
                campaign_id = args.get('campaign_id')
                influencer_id = args.get('influencer_id')
                requirements = args.get('requirements')
                payment_amount = args.get('payment_amount')
                status = args.get('status')
                print(3333333333333333333333)
                print(status)

                adrequest.campaign_id = campaign_id if campaign_id else adrequest.campaign_id
                adrequest.influencer_id = influencer_id if influencer_id else adrequest.influencer_id
                adrequest.requirements = requirements if requirements else adrequest.requirements
                adrequest.payment_amount = payment_amount if payment_amount else adrequest.payment_amount
                adrequest.status = status if status else adrequest.status

                print(status)
                print(campaign_id)

                db.session.commit()
                json_response = {
                    "status_code": 200,
                    "message": "Adreqeuest updated successfully.",
                }
                return jsonify(json_response)

            except Exception as e:
                db.session.rollback()
                json_response = {
                    "status_code": 500,
                    "message": str(e)
                }
                return jsonify(json_response)
        else:
            return jsonify({
                "status_code": 404,
                "message": "adrequest not found."
            })

    def delete(self,id):
        adrequest=AdRequest.query.filter_by(id=id).first()
        db.session.delete(adrequest)
        db.session.commit()
        return adrequest,200

create_msg_parser = reqparse.RequestParser()
create_msg_parser.add_argument('campaign_id')
create_msg_parser.add_argument('influencer_id')
create_msg_parser.add_argument('messages')
create_msg_parser.add_argument('ad_id')
create_msg_parser.add_argument('sponsor_id')
class InserttoMessages(Resource):
    @jwt_required()
    def post(self):
        try:
            user = get_jwt_identity()
            print(user)
            uid = user['id']
            userdata = User.query.filter_by(id=uid).first()
            sender =''
            if userdata.role=='influencer':
                sender='influencer'
                influencer_id=uid
                print(122222222222)
            else:
                sender ='sponsor'
                sponsor_id=uid
                print(2222222222222222333333333333)
            # print(sponsor_id,"sponsor_id")
            args = create_msg_parser.parse_args()
            print(args)
            campaign_id = args.get('campaign_id') if args.get('campaign_id') else ''
            influencer_id = args.get('influencer_id')
            messages = args.get('messages') if args.get('messages') else ''
            ad_id = args.get('ad_id') if args.get('ad_id') else ''
            sponsor_id = args.get('sponsor_id')
            print(sponsor_id,"spid")
            new_msg = Messages(campaign_id=campaign_id,influencer_id=influencer_id,sponsor_id=sponsor_id, messages=messages,ad_id=ad_id,sender=sender)
            db.session.add(new_msg)
            db.session.commit()

            if new_msg:
                json_response = {
                    "status_code":200,
                    "data": new_msg.to_dict(),
                    "message": "Message created successfully",
                }
                return jsonify(json_response)
            else:
                json_response = {   
                    "status_code":400,
                    "data": {},
                    "message": "Message not created.",
                }
                return jsonify(json_response)

        except Exception as e:
            db.session.rollback()
            json_response = {
                "status_code":500,
                "data": {},
                "message": str(e)}
            return jsonify(json_response)
        
    
create_getmsg_parser = reqparse.RequestParser()
create_getmsg_parser.add_argument('campaign_id')
create_getmsg_parser.add_argument('influencer_id')
create_getmsg_parser.add_argument('sponsor_id')

class GetAllMessages(Resource):
    def post(self):
        try:
            print(111111111111)
            args = create_getmsg_parser.parse_args()
            campaign_id = args.get('campaign_id') if args.get('campaign_id') else ''
            print(22222222222222)
            influencer_id = args.get('influencer_id') if args.get('influencer_id') else ''
            sponsor_id = args.get('sponsor_id') if args.get('sponsor_id') else ''
            msgs=Messages.query.filter_by(campaign_id=campaign_id,influencer_id=influencer_id,sponsor_id=sponsor_id).all()
            sponsorname = SponsorProfile.query.filter_by(user_id=sponsor_id).first()
            influencername = InfluencerProfile.query.filter_by(user_id=influencer_id).first()
            Campaignname = Campaign.query.filter_by(id=campaign_id).first()
            print(5555555)
            msglist=[]
            for msg in msgs:
                msg1=msg.to_dict()
                msg1['sponsor_name']=sponsorname.name
                msg1['influencer_name']=influencername.name
                msg1['campaign_name']=Campaignname.name
                msglist.append(msg1)

            if msglist:
                json_response = {
                    "status_code": 200,
                    "data": msglist,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": {},
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)


create_getpayment_parser = reqparse.RequestParser()
create_getpayment_parser.add_argument('campaign_id')
create_getpayment_parser.add_argument('influencer_id')
create_getpayment_parser.add_argument('sponsor_id')
class GetPaymentStatus(Resource):
    def post(self):
        try:
            print(111111111111)
            args = create_getmsg_parser.parse_args()
            campaign_id = args.get('campaign_id') if args.get('campaign_id') else ''
            print(22222222222222)
            influencer_id = args.get('influencer_id') if args.get('influencer_id') else ''
            sponsor_id = args.get('sponsor_id') if args.get('sponsor_id') else ''
            payment=Payments.query.filter_by(campaign_id=campaign_id,influencer_id=influencer_id,sponsor_id=sponsor_id).first()

            if payment:
                json_response = {
                    "status_code": 200,
                    "data": payment.to_dict(),
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": {},
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

# def GetMessagesBySponsorId(Resource):
#     def get(self,id):
#         try:
#             adrequest=AdRequest.query.filter_by(id=id).first()
#             campid = adrequest.campaign_id
#             campaign = Campaign.query.filter_by(id = campid).first()
#             spid = adrequest.sponsor_id
#             spnosor = SponsorProfile.query.filter_by( user_id = spid).first()
#             infid = adrequest.influencer_id
#             influencer = InfluencerProfile.query.filter_by( id = infid).first()
#             adrequest_dict = adrequest.to_dict()
#             adrequest_dict['campaign_name'] = campaign.name
#             adrequest_dict['sponsor_name'] = spnosor.name
#             adrequest_dict['influencer_name'] = influencer.name
#             if adrequest_dict:
#                 json_response = {
#                     "status_code": 200,
#                     "data": adrequest_dict,
#                     "message": "Data fetched."
#                 }
#                 return jsonify(json_response)
#             else:
#                 json_response = {
#                     "status_code": 200,
#                     "data": {},
#                     "message": "Data not fetched."
#                 }
#                 return jsonify(json_response)
            
#         except Exception as e:
#             json_response = {
#                 "status_code": 500,
#                 "data": {},
#                 "message": str(e)
#             }
#             return jsonify(json_response)


class GetAdRequestListBySponsorIdAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            sponsor = get_jwt_identity()
            sponsor_id = sponsor['id']
            adrequests = AdRequest.query.filter_by(sponsor_id=sponsor_id).order_by(AdRequest.id.desc()).all()
            adrequest_list = [adrequest.to_dict() for adrequest in adrequests]
            adrequest_final_list =[]
            for adrequest in adrequest_list:
                campaign = Campaign.query.filter_by(id=adrequest['campaign_id']).first()
                campaign = campaign.to_dict()
                influencer = InfluencerProfile.query.filter_by(user_id=adrequest['influencer_id']).first()
                influencer=influencer.to_dict()
                adrequest['campaign_name']=campaign['name']
                adrequest['influencer_name']=influencer['name']
                adrequest_final_list.append(adrequest)
            # print(adrequest_final_list)
            if adrequest_final_list:
                json_response = {
                    "status_code": 200,
                    "data": adrequest_final_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

class GetAdRequestListByInfluencerIdAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            inf = get_jwt_identity()
            inf_id = inf['id']
            adrequests = AdRequest.query.filter_by(influencer_id=inf_id).order_by(AdRequest.id.desc()).all()
            adrequest_list = [adrequest.to_dict() for adrequest in adrequests]
            # print(adrequest_list)
            adrequest_final_list =[]
            
            for adrequest in adrequest_list:
                campaign = Campaign.query.filter_by(id=adrequest['campaign_id']).first()
                print(campaign)
                campaign = campaign.to_dict()
                sponsor = SponsorProfile.query.filter_by(user_id=adrequest['sponsor_id']).first()
                sponsor=sponsor.to_dict()
                print(5555555555555555555555)
                adrequest['campaign_name']=campaign['name']
                adrequest['sponsor_name']=sponsor['name']
                adrequest_final_list.append(adrequest)
                print(111111111111111111111)
            print(adrequest_final_list)
            if adrequest_final_list:
                json_response = {
                    "status_code": 200,
                    "data": adrequest_final_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": {},
                "message": str(e)
            }
            return jsonify(json_response)

####################### SponsorDashboardSearchAPI ######################

sponsor_search_parser= reqparse.RequestParser()
sponsor_search_parser.add_argument('searchquery')
class SponsorDashboardSearchAPI(Resource):
    def post(self):
        try:
            args = sponsor_search_parser.parse_args()
            search_query = args.get('searchquery')
            search_results_influencers1 = InfluencerProfile.query.filter(InfluencerProfile.name.ilike(f"%{search_query}%")).all()
            search_results_influencers2 = User.query.filter(User.username.ilike(f"%{search_query}%"),User.role == "influencer").all()
            influencer_userid_list = []
            influencer_userid_list.extend(influencer.id for influencer in search_results_influencers2)
            influencer_userid_list.extend(influencer.user_id for influencer in search_results_influencers1)
            influencer_userid_list = list(set(influencer_userid_list))
            influencers_list=[]
            for id in influencer_userid_list:
                infl = InfluencerProfile.query.filter_by(user_id = id).first()
                if infl:
                    influencers_list.append(infl.to_dict())
            # print(influencers_list)
            if influencers_list:
                json_response = {
                    "status_code": 200,
                    "data": influencers_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": [],
                "message": str(e)
            }
            return jsonify(json_response)

####################### class InfluencerDashboardSearchAPI ######################
inf_search_parser= reqparse.RequestParser()
inf_search_parser.add_argument('searchquery')

    
class InfluencerDashboardSearchAPI(Resource):
    def post(self):
        try:
            args = sponsor_search_parser.parse_args()
            search_query = args.get('searchquery')
            result_campaigns = Campaign.query.filter(Campaign.name.ilike(f"%{search_query}%"), Campaign.visibility == "public").all()
            campaigns_list = [campaign.to_dict() for campaign in result_campaigns]
            # print(result_campaigns)
            if campaigns_list:
                json_response = {
                    "status_code": 200,
                    "data": campaigns_list,
                    "message": "Data fetched."
                }
                return jsonify(json_response)
            else:
                json_response = {
                    "status_code": 200,
                    "data": [],
                    "message": "Data not fetched."
                }
                return jsonify(json_response)
            
        except Exception as e:
            json_response = {
                "status_code": 500,
                "data": [],
                "message": str(e)
            }
            return jsonify(json_response)

######################## Admin APIs for Statistics ##############################
    
class AdminAPI(Resource):
    def post(self):
        pass

    def get(self):
        try:
            total_campaign = Campaign.query.count()
            total_adrequest = AdRequest.query.count()
            total_sponsors = User.query.filter_by(role='sponsor', status='approved').count()
            print("111111",total_sponsors)
            total_influencer = User.query.filter_by(role='influencer', status='approved').count()
            print("22222",total_influencer)
            pending_sponsor_accounts = User.query.filter_by(status='pending').order_by(User.id.desc()).all()

            pending_sponsor_accounts_dicts = [user.to_dict() for user in pending_sponsor_accounts]

            return jsonify({
                "total_campaign": total_campaign,
                "total_adrequest":total_adrequest,
                "total_sponsors": total_sponsors,
                "total_influencers": total_influencer,
                "pending_sponsor_accounts": pending_sponsor_accounts_dicts
            })
        except Exception as e:
            return {"error": str(e)}, 500

# Scheduled Jobs- Daily Reminder Jobs APIs
    
class DailyReminderAPI(Resource):
    def post(self):
        pass
    def get(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

# Scheduled Job - Monthly Activity Report APIs
    
class MonthlyActivityReportAPI(Resource):
    def post(self):
        pass
    def get(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

