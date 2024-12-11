import uuid
from datetime import datetime, timezone
from application.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    is_inappropriate = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    sponsor_profile = db.relationship('SponsorProfile', back_populates='user', uselist=False)
    influencer_profile = db.relationship('InfluencerProfile', back_populates='user', uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "is_inappropriate": self.is_inappropriate,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class SponsorProfile(db.Model):
    __tablename__ = 'sponsor_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    contact_email = db.Column(db.String(100))
    website_link = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    user = db.relationship('User', back_populates='sponsor_profile')
    campaigns = db.relationship('Campaign', back_populates='sponsor', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "industry": self.industry,
            "budget": self.budget,
            "contact_email": self.contact_email,
            "website_link": self.website_link,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class InfluencerProfile(db.Model):
    __tablename__ = 'influencer_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    niche = db.Column(db.String(50), nullable=False)
    youtube_follower = db.Column(db.String(20))
    youtube_link = db.Column(db.String(255))
    instagram_follower = db.Column(db.String(20))
    instagram_link = db.Column(db.String(255))
    twitter_follower = db.Column(db.String(20))
    twitter_link = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    user = db.relationship('User', back_populates='influencer_profile')
    ad_requests = db.relationship('AdRequest', back_populates='influencer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "category": self.category,
            "niche": self.niche,
            "youtube_follower": self.youtube_follower,
            "youtube_link": self.youtube_link,
            "instagram_follower": self.instagram_follower,
            "instagram_link": self.instagram_link,
            "twitter_follower": self.twitter_follower,
            "twitter_link": self.twitter_link,
            "user_id": self.user_id,
            # "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    primary_goal = db.Column(db.Text, nullable=True)
    secondary_goal = db.Column(db.Text, nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    impressions = db.Column(db.Integer, nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profiles.id'), nullable=False)
    is_inappropriate = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    sponsor = db.relationship('SponsorProfile', back_populates='campaigns')
    ad_requests = db.relationship('AdRequest', back_populates='campaign', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.strftime('%Y-%m-%d') if isinstance(self.start_date, datetime) else self.start_date,
            "end_date": self.end_date.strftime('%Y-%m-%d') if isinstance(self.end_date, datetime) else self.end_date,
            "budget": self.budget,
            "visibility": self.visibility,
            "primary_goal": self.primary_goal,
            "secondary_goal": self.secondary_goal,
            "clicks": self.clicks if self.clicks else 0,
            "impressions": self.impressions if self.impressions else 0,
            "sponsor_id": self.sponsor_id,
            "is_inappropriate": self.is_inappropriate,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profiles.user_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profiles.user_id'), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    campaign = db.relationship('Campaign', back_populates='ad_requests')
    influencer = db.relationship('InfluencerProfile', back_populates='ad_requests')

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "campaign_id": self.campaign_id,
            "sponsor_id": self.sponsor_id,
            "influencer_id": self.influencer_id,
            "requirements": self.requirements,
            "payment_amount": self.payment_amount,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class Messages(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    campaign_id = db.Column(db.Integer, nullable=True)
    sponsor_id = db.Column(db.Integer, nullable=False)
    influencer_id = db.Column(db.Integer, nullable=False)
    messages = db.Column(db.Text, nullable=True)
    ad_id = db.Column(db.Integer,nullable=True)
    sender = db.Column(db.Integer,nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "campaign_id": self.campaign_id,
            "sponsor_id": self.sponsor_id,
            "influencer_id": self.influencer_id,
            "messages": self.messages,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.created_at, datetime) else self.created_at
        }

class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    influencer_id = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer, nullable=False)
    campaign_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "influencers_user_id": self.influencer_id,
            "sponsors_user_id": self.sponsor_id,
            "campaign_id":self.campaign_id,
            "amount_received": self.amount,
            "created_at": self.created_at
        }
