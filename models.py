from app import db
from datetime import datetime
from sqlalchemy import Text, DateTime, Float

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    content = db.Column(Text, nullable=False)
    upload_date = db.Column(DateTime, default=datetime.utcnow)
    
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
    
    resume = db.relationship('Resume', backref='analyses')
    job = db.relationship('Job', backref='analyses')
