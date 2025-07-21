import os
import uuid
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
from app import app, db
from models import Resume, Job, Analysis, User
from document_parser import DocumentParser
from resume_analyzer import ResumeAnalyzer
from gamification import GamificationService
import logging

logger = logging.getLogger(__name__)

# Initialize services
analyzer = ResumeAnalyzer()
gamification = GamificationService()

def get_current_user():
    """Get or create current user based on session"""
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())
    
    return gamification.get_or_create_user(session['user_session_id'])

# Sample job data for demonstration
SAMPLE_JOBS = [
    {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "description": "We are looking for a Senior Software Engineer to join our dynamic team. You will be responsible for developing scalable web applications and leading technical initiatives.",
        "requirements": "5+ years of experience in Python, JavaScript, React, AWS, Docker, experience with microservices architecture, strong problem-solving skills, team leadership experience.",
        "location": "San Francisco, CA"
    },
    {
        "title": "Data Scientist",
        "company": "Analytics Inc",
        "description": "Join our data science team to build machine learning models and derive insights from large datasets to drive business decisions.",
        "requirements": "PhD in Computer Science or related field, Python, R, SQL, machine learning frameworks (TensorFlow, PyTorch), statistical analysis, data visualization, 3+ years experience.",
        "location": "Remote"
    },
    {
        "title": "Product Manager",
        "company": "Innovation Labs",
        "description": "Lead product development from conception to launch, working closely with engineering, design, and marketing teams.",
        "requirements": "MBA preferred, 4+ years product management experience, agile methodologies, user research, product analytics, cross-functional team leadership, market analysis.",
        "location": "New York, NY"
    }
]

def populate_sample_jobs():
    """Populate database with sample jobs if empty"""
    if Job.query.count() == 0:
        for job_data in SAMPLE_JOBS:
            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                description=job_data["description"],
                requirements=job_data["requirements"],
                location=job_data["location"]
            )
            db.session.add(job)
        db.session.commit()

@app.route('/')
def index():
    """Home page with gamification data"""
    populate_sample_jobs()
    user = get_current_user()
    
    # Update daily streak
    gamification.update_streak(user)
    
    # Get user stats for dashboard
    user_stats = gamification.get_user_stats(user)
    
    # Get recent achievements
    recent_badges = []
    if user.user_badges:
        recent_badges = sorted(user.user_badges, key=lambda x: x.earned_date, reverse=True)[:3]
    
    return render_template('index.html', 
                         user_stats=user_stats, 
                         recent_badges=recent_badges,
                         user=user)

@app.route('/upload')
def upload_page():
    """Resume upload page"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and initial processing"""
    try:
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not DocumentParser.is_supported_format(file.filename):
            flash('Unsupported file format. Please upload PDF or DOCX files.', 'error')
            return redirect(request.url)
        
        # Generate unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse document
        file_extension = os.path.splitext(file.filename)[1]
        content = DocumentParser.parse_document(file_path, file_extension)
        
        if not content.strip():
            flash('Could not extract text from the document. Please ensure the file is not corrupted.', 'error')
            os.remove(file_path)
            return redirect(request.url)
        
        # Get current user for gamification
        user = get_current_user()
        
        # Save to database
        resume = Resume(
            filename=filename,
            original_filename=secure_filename(file.filename),
            content=content,
            user_id=user.id
        )
        db.session.add(resume)
        db.session.commit()
        
        # Store resume ID in session
        session['resume_id'] = resume.id
        
        # Award XP and check achievements
        level_up_data = gamification.award_xp(user, gamification.XP_RESUME_UPLOAD, "Resume Upload")
        achievements = gamification.check_achievements(user, {'action': 'resume_upload'})
        
        flash('Resume uploaded successfully!', 'success')
        return redirect(url_for('analyze_resume'))
        
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        flash(f'Error processing resume: {str(e)}', 'error')
        return redirect(request.url)

@app.route('/analyze')
def analyze_resume():
    """Resume analysis page"""
    resume_id = session.get('resume_id')
    if not resume_id:
        flash('Please upload a resume first', 'error')
        return redirect(url_for('upload_page'))
    
    resume = Resume.query.get_or_404(resume_id)
    return render_template('results.html', resume=resume, analysis=None)

@app.route('/analyze', methods=['POST'])
def perform_analysis():
    """Perform AI analysis of resume"""
    try:
        resume_id = session.get('resume_id')
        if not resume_id:
            flash('Please upload a resume first', 'error')
            return redirect(url_for('upload_page'))
        
        resume = Resume.query.get_or_404(resume_id)
        job_description = request.form.get('job_description', '').strip()
        
        # Perform AI analysis
        if job_description:
            analysis_result = analyzer.analyze_resume(resume.content, job_description)
        else:
            analysis_result = analyzer.analyze_resume(resume.content)
        
        # Get current user for gamification
        user = get_current_user()
        
        # Award XP based on score improvement and first analysis
        score = analysis_result.get('overall_score', 0)
        xp_amount = gamification.XP_FIRST_ANALYSIS
        if resume.current_score > 0:
            improvement = score - resume.current_score
            if improvement > 0:
                xp_amount += gamification.XP_SCORE_IMPROVEMENT(improvement)
        
        # Update resume score
        resume.current_score = score
        
        # Save analysis to database
        analysis = Analysis(
            resume_id=resume.id,
            overall_score=analysis_result.get('overall_score', 0),
            skills_match_score=analysis_result.get('skills_match_score', analysis_result.get('content_quality_score', 0)),
            experience_match_score=analysis_result.get('experience_match_score', analysis_result.get('structure_score', 0)),
            education_match_score=analysis_result.get('education_match_score', analysis_result.get('completeness_score', 0)),
            recommendations='\n'.join(analysis_result.get('recommendations', [])),
            missing_skills='\n'.join(analysis_result.get('missing_skills', analysis_result.get('missing_sections', []))),
            xp_awarded=xp_amount
        )
        db.session.add(analysis)
        db.session.commit()
        
        # Award XP and check achievements
        level_up_data = gamification.award_xp(user, xp_amount, "Resume Analysis")
        achievements = gamification.check_achievements(user, {'action': 'analysis_complete', 'score': score})
        
        return render_template('results.html', resume=resume, analysis=analysis, analysis_data=analysis_result, 
                             level_up_data=level_up_data, achievements=achievements)
        
    except Exception as e:
        logger.error(f"Error performing analysis: {str(e)}")
        flash(f'Error analyzing resume: {str(e)}', 'error')
        return redirect(url_for('analyze_resume'))

@app.route('/jobs')
def job_listings():
    """Job listings page"""
    populate_sample_jobs()
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/match-jobs')
def match_jobs():
    """Match current resume against all jobs"""
    try:
        resume_id = session.get('resume_id')
        if not resume_id:
            flash('Please upload a resume first', 'error')
            return redirect(url_for('upload_page'))
        
        resume = Resume.query.get_or_404(resume_id)
        jobs = Job.query.all()
        job_matches = []
        
        for job in jobs:
            try:
                match_result = analyzer.calculate_job_match_score(
                    resume.content, 
                    f"{job.title}\n{job.description}\n{job.requirements}"
                )
                job_matches.append({
                    'job': job,
                    'match_score': match_result.get('match_score', 0),
                    'recommendation': match_result.get('recommendation', 'Unknown'),
                    'matching_keywords': match_result.get('matching_keywords', []),
                    'gap_analysis': match_result.get('gap_analysis', [])
                })
            except Exception as e:
                logger.error(f"Error matching job {job.id}: {str(e)}")
                job_matches.append({
                    'job': job,
                    'match_score': 0,
                    'recommendation': 'Error',
                    'matching_keywords': [],
                    'gap_analysis': ['Unable to analyze match']
                })
        
        # Sort by match score
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return render_template('jobs.html', jobs=jobs, job_matches=job_matches, resume=resume)
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        flash(f'Error matching jobs: {str(e)}', 'error')
        return redirect(url_for('job_listings'))

@app.route('/clear-session')
def clear_session():
    """Clear session data"""
    session.clear()
    flash('Session cleared. You can upload a new resume.', 'info')
    return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload a file smaller than 16MB.', 'error')
    return redirect(url_for('upload_page'))

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server Error: {e}", exc_info=True)
    return render_template('500.html'), 500
