# 🚀 AI Resume Analyzer & Job Matching Platform

A gamified AI-powered resume analyzer that helps job seekers optimize their resumes and discover ideal career opportunities.

![Resume Analyzer Demo](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-lightgrey)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-black)

## ✨ Features

### 🎯 Core Functionality
- **AI-Powered Analysis**: Comprehensive resume scoring using OpenAI GPT-4o
- **Intelligent Fallback**: Works even without AI API - provides meaningful analysis
- **Job Matching**: Compatibility scoring against job postings
- **Multi-Format Support**: Upload PDF and DOCX resume files
- **ATS Compatibility**: Analysis for Applicant Tracking Systems

### 🎮 Gamification System
- **XP & Leveling**: Earn experience points for actions (upload: 25 XP, analysis: 50+ XP)
- **Achievement Badges**: Unlock badges for milestones and accomplishments
- **Progress Tracking**: Visual level progression with animated progress bars
- **Daily Missions**: Complete tasks to earn bonus XP rewards
- **Stats Dashboard**: Track uploaded resumes, total XP, and current streak

### 🎨 Modern UI/UX
- **Dopamine-Triggering Design**: Celebration effects and visual rewards
- **Dark Theme**: Professional dark mode with custom color palette
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Bootstrap 5**: Modern, accessible component library

## 🛠 Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with Supabase
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **AI Integration**: OpenAI API (GPT-4o)
- **File Processing**: PyPDF2, python-docx

### Frontend
- **Templating**: Jinja2
- **Styling**: Bootstrap 5 with custom dark theme
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS for interactions

### Deployment
- **Platform**: Vercel (Serverless)
- **Database**: Supabase (PostgreSQL)
- **File Storage**: Vercel filesystem
- **Environment**: Production-ready configuration

## 🚀 Quick Start

### Live Demo
Visit the live application: [AI Resume Analyzer](https://your-app-name.vercel.app)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
export DATABASE_URL="your_supabase_connection_string"
export SESSION_SECRET="your-secret-key"
export OPENAI_API_KEY="sk-your-openai-key"  # Optional
```

4. **Run the application**
```bash
python main.py
```

5. **Open in browser**
Navigate to `http://localhost:5000`

## 📱 How to Use

1. **Upload Resume**: Drag and drop your PDF or DOCX resume
2. **Get Analysis**: Receive detailed scoring and recommendations
3. **Earn XP**: Gain experience points for every action
4. **Unlock Badges**: Achieve milestones to unlock new badges
5. **Track Progress**: Monitor your improvement over time
6. **Match Jobs**: Compare your resume against job postings

## 🎯 Analysis Features

### Resume Scoring
- **Overall Score** (0-100): Comprehensive resume quality
- **Skills Match**: Relevance of technical skills
- **Experience Match**: Professional experience alignment
- **Education Fit**: Educational background relevance
- **ATS Compatibility**: Applicant Tracking System optimization

### Detailed Feedback
- **Strengths**: What your resume does well
- **Weaknesses**: Areas needing improvement
- **Recommendations**: Specific actionable advice
- **Missing Skills**: Skills to add for better job matching
- **Keywords Analysis**: Important terms found and missing

## 🏆 Gamification Elements

### Experience Points
- Resume Upload: **25 XP**
- Complete Analysis: **50-75 XP** (based on score)
- Job Matching: **30 XP**
- Profile Updates: **15 XP**

### Badge System
- 🏅 **First Steps**: Upload your first resume
- 🎯 **High Achiever**: Score above 90%
- 🔥 **On Fire**: 7-day upload streak
- 📈 **Improving**: Show score improvement
- ⚡ **Power User**: Complete 10+ analyses

## 📊 Database Schema

### Core Models
- **User**: Session-based user tracking
- **Resume**: Uploaded resume files and content
- **Analysis**: AI-generated analysis results
- **Job**: Job postings and requirements

### Gamification Models
- **Badge**: Available achievement badges
- **UserBadge**: User badge relationships
- **Challenge**: Available challenges/missions
- **UserChallenge**: User challenge progress
- **Achievement**: Milestone tracking

## 🔧 Configuration

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@host:port/db
SESSION_SECRET=your-secret-key
OPENAI_API_KEY=sk-your-openai-key  # Optional
```

### File Upload Settings
- Maximum file size: 16MB
- Supported formats: PDF, DOCX
- Upload directory: `uploads/`

## 🚀 Deployment Guide

Complete deployment instructions available in [GITHUB_VERCEL_DEPLOYMENT.md](GITHUB_VERCEL_DEPLOYMENT.md)

### Quick Deploy to Vercel
1. Fork this repository
2. Connect to Vercel
3. Add environment variables
4. Deploy automatically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/ai-resume-analyzer/issues)
- **Documentation**: Check the `DEPLOYMENT.md` file
- **Contact**: Create an issue for questions

## 🎉 Acknowledgments

- OpenAI for GPT-4o API
- Supabase for database hosting
- Vercel for serverless deployment
- Bootstrap team for the UI framework
- Font Awesome for icons

---

**Made with ❤️ for job seekers worldwide**

Transform your resume into a career-boosting tool with AI-powered insights and gamified improvement tracking!