from app import db
from datetime import datetime
from sqlalchemy import Text, DateTime, Float, Integer, Boolean, JSON

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120))
    career_level = db.Column(db.Integer, default=1)
    total_xp = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity = db.Column(DateTime, default=datetime.utcnow)
    avatar_config = db.Column(JSON, default={})
    created_date = db.Column(DateTime, default=datetime.utcnow)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    content = db.Column(Text, nullable=False)
    upload_date = db.Column(DateTime, default=datetime.utcnow)
    current_score = db.Column(Float, default=0)
    
    user = db.relationship('User', backref='resumes')
    
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    description = db.Column(Text, nullable=False)
    requirements = db.Column(Text, nullable=False)
    location = db.Column(db.String(100))
    posted_date = db.Column(DateTime, default=datetime.utcnow)
    
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    overall_score = db.Column(Float, nullable=False)
    skills_match_score = db.Column(Float)
    experience_match_score = db.Column(Float)
    education_match_score = db.Column(Float)
    recommendations = db.Column(Text)
    missing_skills = db.Column(Text)
    analysis_date = db.Column(DateTime, default=datetime.utcnow)
    xp_awarded = db.Column(db.Integer, default=0)
    
    resume = db.relationship('Resume', backref='analyses')
    job = db.relationship('Job', backref='analyses')

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # skill, achievement, milestone, special
    rarity = db.Column(db.String(20), default='common')  # common, rare, epic, legendary
    xp_value = db.Column(db.Integer, default=10)
    unlock_condition = db.Column(JSON)  # Conditions to unlock this badge
    created_date = db.Column(DateTime, default=datetime.utcnow)

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_date = db.Column(DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='user_badges')
    badge = db.relationship('Badge', backref='user_badges')

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(Text, nullable=False)
    challenge_type = db.Column(db.String(50), nullable=False)  # daily, weekly, monthly, special
    xp_reward = db.Column(db.Integer, default=50)
    badge_reward_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=True)
    start_date = db.Column(DateTime, default=datetime.utcnow)
    end_date = db.Column(DateTime)
    is_active = db.Column(Boolean, default=True)
    completion_criteria = db.Column(JSON)
    
    badge_reward = db.relationship('Badge', backref='challenges')

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    progress = db.Column(JSON, default={})
    completed = db.Column(Boolean, default=False)
    completed_date = db.Column(DateTime)
    
    user = db.relationship('User', backref='user_challenges')
    challenge = db.relationship('Challenge', backref='user_challenges')

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_type = db.Column(db.String(100), nullable=False)
    achievement_data = db.Column(JSON)
    xp_earned = db.Column(db.Integer, default=0)
    created_date = db.Column(DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='achievements')
