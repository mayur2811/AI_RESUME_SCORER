"""
Gamification Service - Handles all game mechanics, progression, badges, and achievements
"""
from models import User, Badge, UserBadge, Challenge, UserChallenge, Achievement, Analysis
from app import db
from datetime import datetime, timedelta
import json

class GamificationService:
    
    # XP and Level Configuration
    XP_PER_LEVEL = 100
    MAX_LEVEL = 100
    
    # XP Rewards
    XP_RESUME_UPLOAD = 25
    XP_FIRST_ANALYSIS = 50
    XP_SCORE_IMPROVEMENT = lambda self, improvement: int(improvement * 2)
    XP_DAILY_LOGIN = 10
    XP_STREAK_BONUS = 5
    
    def __init__(self):
        self._badges_initialized = False
    
    def get_or_create_user(self, session_id):
        """Get or create user based on session ID"""
        if not self._badges_initialized:
            self.initialize_default_badges()
            self._badges_initialized = True
            
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            user = User(session_id=session_id)
            db.session.add(user)
            db.session.commit()
            # Award welcome badge
            self.award_badge(user, 'welcome_aboard')
        return user
    
    def calculate_level(self, total_xp):
        """Calculate level based on total XP"""
        if total_xp < 0:
            return 1
        level = min(int(total_xp / self.XP_PER_LEVEL) + 1, self.MAX_LEVEL)
        return level
    
    def calculate_xp_for_next_level(self, current_level):
        """Calculate XP needed for next level"""
        if current_level >= self.MAX_LEVEL:
            return 0
        return current_level * self.XP_PER_LEVEL
    
    def award_xp(self, user, xp_amount, reason="General"):
        """Award XP to user and check for level up"""
        old_level = user.career_level
        user.total_xp += xp_amount
        new_level = self.calculate_level(user.total_xp)
        
        level_up_data = None
        if new_level > old_level:
            user.career_level = new_level
            level_up_data = {
                'old_level': old_level,
                'new_level': new_level,
                'xp_gained': xp_amount,
                'reason': reason
            }
            # Award level milestone badges
            self.check_level_milestones(user, new_level)
        
        user.last_activity = datetime.utcnow()
        db.session.commit()
        
        # Log achievement
        achievement = Achievement(
            user_id=user.id,
            achievement_type='xp_earned',
            achievement_data={'xp': xp_amount, 'reason': reason},
            xp_earned=xp_amount
        )
        db.session.add(achievement)
        db.session.commit()
        
        return level_up_data
    
    def award_badge(self, user, badge_name):
        """Award a badge to user if they don't already have it"""
        badge = Badge.query.filter_by(name=badge_name).first()
        if not badge:
            return False
            
        # Check if user already has this badge
        existing = UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first()
        if existing:
            return False
        
        # Award the badge
        user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
        db.session.add(user_badge)
        
        # Award XP for the badge
        self.award_xp(user, badge.xp_value, f"Badge: {badge.name}")
        
        db.session.commit()
        return True
    
    def check_achievements(self, user, context_data=None):
        """Check and award achievements based on user actions"""
        achievements_awarded = []
        
        if context_data:
            # Resume upload achievements
            if context_data.get('action') == 'resume_upload':
                if user.resumes.count() == 1:
                    if self.award_badge(user, 'first_resume'):
                        achievements_awarded.append('first_resume')
                elif user.resumes.count() == 5:
                    if self.award_badge(user, 'resume_collector'):
                        achievements_awarded.append('resume_collector')
            
            # Analysis achievements
            elif context_data.get('action') == 'analysis_complete':
                score = context_data.get('score', 0)
                analyses_count = user.resumes[0].analyses.count() if user.resumes else 0
                
                if analyses_count == 1:
                    if self.award_badge(user, 'first_analysis'):
                        achievements_awarded.append('first_analysis')
                
                # Score-based achievements
                if score >= 90:
                    if self.award_badge(user, 'perfectionist'):
                        achievements_awarded.append('perfectionist')
                elif score >= 80:
                    if self.award_badge(user, 'high_achiever'):
                        achievements_awarded.append('high_achiever')
                elif score >= 70:
                    if self.award_badge(user, 'skilled_professional'):
                        achievements_awarded.append('skilled_professional')
        
        return achievements_awarded
    
    def check_level_milestones(self, user, level):
        """Check and award milestone badges for reaching certain levels"""
        milestones = {
            5: 'level_5_rookie',
            10: 'level_10_rising_star',
            25: 'level_25_professional',
            50: 'level_50_expert',
            75: 'level_75_master',
            100: 'level_100_legend'
        }
        
        if level in milestones:
            self.award_badge(user, milestones[level])
    
    def update_streak(self, user):
        """Update user's daily streak"""
        today = datetime.utcnow().date()
        last_activity_date = user.last_activity.date() if user.last_activity else None
        
        if not last_activity_date:
            user.current_streak = 1
        elif last_activity_date == today:
            # Already logged in today
            return user.current_streak
        elif last_activity_date == today - timedelta(days=1):
            # Consecutive day
            user.current_streak += 1
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
        else:
            # Streak broken
            user.current_streak = 1
        
        # Award streak badges
        if user.current_streak == 7:
            self.award_badge(user, 'week_warrior')
        elif user.current_streak == 30:
            self.award_badge(user, 'month_master')
        elif user.current_streak == 100:
            self.award_badge(user, 'streak_legend')
        
        user.last_activity = datetime.utcnow()
        db.session.commit()
        
        return user.current_streak
    
    def get_user_stats(self, user):
        """Get comprehensive user statistics for dashboard"""
        current_level = user.career_level
        xp_for_current_level = (current_level - 1) * self.XP_PER_LEVEL
        xp_for_next_level = current_level * self.XP_PER_LEVEL
        xp_progress = user.total_xp - xp_for_current_level
        xp_needed = xp_for_next_level - user.total_xp
        
        return {
            'level': current_level,
            'total_xp': user.total_xp,
            'xp_progress': xp_progress,
            'xp_needed': max(0, xp_needed),
            'xp_for_level': self.XP_PER_LEVEL,
            'progress_percentage': min(100, (xp_progress / self.XP_PER_LEVEL) * 100),
            'current_streak': user.current_streak,
            'longest_streak': user.longest_streak,
            'badges_count': len(user.user_badges),
            'resumes_count': len(user.resumes),
            'level_title': self.get_level_title(current_level)
        }
    
    def get_level_title(self, level):
        """Get title based on level"""
        if level < 10:
            return "Resume Novice"
        elif level < 20:
            return "Career Explorer"
        elif level < 30:
            return "Job Seeker"
        elif level < 40:
            return "Professional"
        elif level < 50:
            return "Career Expert"
        elif level < 60:
            return "Industry Specialist"
        elif level < 70:
            return "Senior Professional"
        elif level < 80:
            return "Career Master"
        elif level < 90:
            return "Executive Leader"
        elif level < 100:
            return "Career Legend"
        else:
            return "Resume Grandmaster"
    
    def initialize_default_badges(self):
        """Initialize default badges if they don't exist"""
        default_badges = [
            {
                'name': 'welcome_aboard',
                'description': 'Welcome to your career journey!',
                'icon': 'fas fa-rocket',
                'category': 'milestone',
                'rarity': 'common',
                'xp_value': 10
            },
            {
                'name': 'first_resume',
                'description': 'Uploaded your first resume',
                'icon': 'fas fa-file-alt',
                'category': 'achievement',
                'rarity': 'common',
                'xp_value': 25
            },
            {
                'name': 'first_analysis',
                'description': 'Completed your first AI analysis',
                'icon': 'fas fa-brain',
                'category': 'achievement',
                'rarity': 'common',
                'xp_value': 50
            },
            {
                'name': 'skilled_professional',
                'description': 'Achieved 70+ resume score',
                'icon': 'fas fa-award',
                'category': 'skill',
                'rarity': 'rare',
                'xp_value': 75
            },
            {
                'name': 'high_achiever',
                'description': 'Achieved 80+ resume score',
                'icon': 'fas fa-trophy',
                'category': 'skill',
                'rarity': 'epic',
                'xp_value': 100
            },
            {
                'name': 'perfectionist',
                'description': 'Achieved 90+ resume score',
                'icon': 'fas fa-crown',
                'category': 'skill',
                'rarity': 'legendary',
                'xp_value': 150
            },
            {
                'name': 'week_warrior',
                'description': '7-day login streak',
                'icon': 'fas fa-fire',
                'category': 'streak',
                'rarity': 'rare',
                'xp_value': 50
            },
            {
                'name': 'month_master',
                'description': '30-day login streak',
                'icon': 'fas fa-calendar-check',
                'category': 'streak',
                'rarity': 'epic',
                'xp_value': 200
            },
            {
                'name': 'level_5_rookie',
                'description': 'Reached Level 5',
                'icon': 'fas fa-star',
                'category': 'milestone',
                'rarity': 'common',
                'xp_value': 25
            },
            {
                'name': 'level_10_rising_star',
                'description': 'Reached Level 10',
                'icon': 'fas fa-star-half-alt',
                'category': 'milestone',
                'rarity': 'rare',
                'xp_value': 50
            },
            {
                'name': 'level_25_professional',
                'description': 'Reached Level 25',
                'icon': 'fas fa-user-tie',
                'category': 'milestone',
                'rarity': 'epic',
                'xp_value': 100
            },
            {
                'name': 'resume_collector',
                'description': 'Uploaded 5 different resumes',
                'icon': 'fas fa-folder-open',
                'category': 'achievement',
                'rarity': 'rare',
                'xp_value': 75
            }
        ]
        
        for badge_data in default_badges:
            existing = Badge.query.filter_by(name=badge_data['name']).first()
            if not existing:
                badge = Badge(**badge_data)
                db.session.add(badge)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing badges: {e}")