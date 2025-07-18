# AI Resume Analyzer

## Overview

This is a Flask-based web application that provides AI-powered resume analysis and job matching capabilities. The system allows users to upload resumes in PDF or DOCX format, analyzes them using OpenAI's API, and provides detailed feedback including compatibility scores with job postings.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### July 18, 2025 - Vercel Deployment Configuration
- Created `vercel.json` configuration for Vercel deployment
- Added `api/index.py` as Vercel entry point following serverless architecture
- Generated `requirements.txt` from pyproject.toml dependencies
- Created comprehensive deployment guide in `DEPLOYMENT.md`
- Configured environment variables for production (DATABASE_URL, OPENAI_API_KEY, SESSION_SECRET)
- Set up proper Python path handling for Vercel's serverless functions

### July 18, 2025 - Enhanced UI Design Implementation
- Implemented comprehensive UI design specification with proper color system
- Updated color palette to match specifications (Primary Blue #4F46E5, Success Green #10B981, etc.)
- Enhanced gamification dashboard with redesigned level progress container and stats grid
- Added "Today's Missions" section with interactive checkboxes and XP rewards
- Created responsive 2x2 stats cards with hover effects and proper spacing
- Improved visual hierarchy and dopamine-triggering design elements

### July 18, 2025 - Comprehensive Gamification System
- Added full gamification models (User, Badge, UserBadge, Challenge, UserChallenge, Achievement)
- Implemented GamificationService with XP system, level progression, and achievement tracking
- Added magical gamified dashboard on homepage showing user level, XP progress, streaks, and badges
- Integrated XP rewards for resume uploads (25 XP) and analysis completion (50+ XP based on score)
- Created badge system with automatic achievement detection for milestones
- Enhanced UI with animated progress bars, level avatars, and celebration effects
- Added session-based user tracking without requiring account creation

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating engine
- **Styling**: Bootstrap 5 with custom dark theme and Font Awesome icons
- **JavaScript**: Vanilla JavaScript for client-side interactions, form validation, and UI enhancements
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Session Management**: Flask's built-in session handling with configurable secret key
- **File Handling**: Werkzeug for secure file uploads with size and type validation
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Data Storage Solutions
- **Primary Database**: SQLite (development) with PostgreSQL support via environment configuration
- **File Storage**: Local filesystem for uploaded resume files
- **Session Storage**: Server-side sessions using Flask's session management

### Authentication and Authorization
- **Current State**: No formal authentication system implemented
- **Session Tracking**: Uses Flask sessions to track uploaded resumes and maintain user context
- **Security**: Basic file upload validation and secure filename handling

## Key Components

### Document Processing
- **DocumentParser Class**: Handles extraction of text content from PDF and DOCX files
- **Supported Formats**: PDF (via PyPDF2) and DOCX (via python-docx)
- **Error Handling**: Comprehensive exception handling for file parsing failures

### AI Analysis Engine
- **ResumeAnalyzer Class**: Integrates with OpenAI API for intelligent resume analysis
- **Analysis Types**: General resume quality assessment and job-specific compatibility scoring
- **Scoring Metrics**: Overall score, skills match, experience match, education match, and ATS compatibility

### Database Models
- **Resume Model**: Stores uploaded resume metadata and extracted content
- **Job Model**: Contains job listings with titles, companies, descriptions, and requirements
- **Analysis Model**: Links resumes to jobs with detailed scoring and recommendations

### Web Interface
- **Upload System**: Secure file upload with validation and progress indication
- **Analysis Dashboard**: Visual presentation of scores and recommendations
- **Job Matching**: Display of compatible job opportunities with ranking

## Data Flow

1. **File Upload**: User uploads resume → File validation → Text extraction → Database storage
2. **Analysis Request**: User initiates analysis → OpenAI API call → Score calculation → Results storage
3. **Job Matching**: System compares resume against job listings → Compatibility scoring → Ranked results
4. **Results Display**: Formatted presentation of scores, recommendations, and job matches

## External Dependencies

### AI Services
- **OpenAI API**: Primary AI engine for resume analysis and job matching
- **Configuration**: API key via environment variable with fallback placeholder

### Document Processing Libraries
- **PyPDF2**: PDF text extraction functionality
- **python-docx**: Microsoft Word document processing

### Web Framework Dependencies
- **Flask Ecosystem**: Core framework, SQLAlchemy ORM, and various extensions
- **Bootstrap**: Frontend styling and responsive components
- **Font Awesome**: Icon library for enhanced UI

### Development Tools
- **Logging**: Comprehensive logging system for debugging and monitoring
- **Environment Configuration**: Environment-based configuration for database and API keys

## Deployment Strategy

### Configuration Management
- **Environment Variables**: Database URL, OpenAI API key, and session secret
- **File Upload Settings**: Configurable upload directory and file size limits
- **Database Options**: Connection pooling and health check configurations

### Production Considerations
- **Database**: Designed to work with PostgreSQL in production while using SQLite for development
- **File Storage**: Currently uses local filesystem (could be extended to cloud storage)
- **Security**: Session secret configuration and secure file handling
- **Scaling**: Database connection pooling and proxy-aware configuration

### Current Limitations
- No user authentication system (sessions are temporary)
- Local file storage only
- Single-server deployment model
- Limited error recovery for AI service failures

The application follows a modular design pattern with clear separation of concerns between document processing, AI analysis, data persistence, and web presentation layers.