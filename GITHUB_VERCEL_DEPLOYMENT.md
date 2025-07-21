# Complete Guide: Deploy Resume Analyzer to GitHub & Vercel

## Prerequisites
- GitHub account (free)
- Vercel account (free) 
- Git installed on your computer

## Step 1: Prepare Your Project Files

Your project is ready! All necessary files are already configured:
- ✅ `vercel.json` - Vercel deployment configuration
- ✅ `api/index.py` - Vercel serverless function entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ Application files (main.py, models.py, etc.)

## Step 2: Upload to GitHub

### 2.1 Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click the green "New" button or go to [Create Repository](https://github.com/new)
3. Fill in repository details:
   - **Repository name**: `ai-resume-analyzer`
   - **Description**: `AI-powered resume analyzer with gamification features`
   - **Visibility**: Public (required for free Vercel deployment)
   - ✅ Check "Add a README file"
4. Click "Create repository"

### 2.2 Upload Files to GitHub
**Option A: Using GitHub Web Interface (Easiest)**
1. In your new repository, click "uploading an existing file"
2. Drag and drop ALL project files from your computer:
   ```
   api/
   static/
   templates/
   uploads/
   app.py
   main.py
   models.py
   gamification.py
   resume_analyzer.py
   document_parser.py
   routes.py
   vercel.json
   requirements.txt
   DEPLOYMENT.md
   ```
3. Write commit message: "Initial commit - AI Resume Analyzer"
4. Click "Commit changes"

**Option B: Using Git Commands**
```bash
# Download project files to your computer first, then:
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
# Copy all project files to this folder
git add .
git commit -m "Initial commit - AI Resume Analyzer"
git push origin main
```

## Step 3: Deploy to Vercel

### 3.1 Connect Vercel to GitHub
1. Go to [Vercel](https://vercel.com)
2. Click "Sign up" and choose "Continue with GitHub"
3. Authorize Vercel to access your GitHub account

### 3.2 Import Your Project
1. On Vercel dashboard, click "New Project"
2. Find your `ai-resume-analyzer` repository
3. Click "Import" next to it

### 3.3 Configure Deployment Settings
1. **Project Name**: Keep as `ai-resume-analyzer` or customize
2. **Framework Preset**: Select "Other" or leave as detected
3. **Root Directory**: Leave empty (use root)
4. **Build Settings**: 
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: Leave empty

### 3.4 Add Environment Variables
Click "Environment Variables" and add these:

**Required Variables:**
1. **DATABASE_URL**
   - Name: `DATABASE_URL`
   - Value: Your Supabase connection string
   - Format: `postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres`

2. **SESSION_SECRET**
   - Name: `SESSION_SECRET`
   - Value: Any random string (e.g., `my-super-secret-key-12345`)

**Optional (for full AI features):**
3. **OPENAI_API_KEY**
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key (starts with `sk-`)
   - Note: App works without this using intelligent fallback

### 3.5 Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://your-project-name.vercel.app`

## Step 4: Set Up Supabase Database

### 4.1 Get Database URL
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard/projects)
2. Select your project: `vdhotrhbvlcntplhsagy`
3. Click "Connect" button
4. Copy the connection string under "Transaction pooler"
5. Replace `[YOUR-PASSWORD]` with your actual database password

### 4.2 Update Environment Variables
1. Go back to Vercel dashboard
2. Click your project → Settings → Environment Variables
3. Update `DATABASE_URL` with your Supabase connection string
4. Click "Save"

## Step 5: Test Your Live Application

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. Test features:
   - ✅ Homepage loads with gamification dashboard
   - ✅ Upload a resume (PDF or DOCX)
   - ✅ Get analysis results and earn XP
   - ✅ View badges and achievements
   - ✅ Check job matching features

## Step 6: Custom Domain (Optional)

1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain (if you have one)
3. Follow DNS configuration instructions

## Troubleshooting

### Common Issues:
1. **Build Fails**: Check requirements.txt includes all dependencies
2. **Database Connection Error**: Verify DATABASE_URL format and password
3. **App Crashes**: Check Vercel Function logs in dashboard
4. **Static Files Not Loading**: Ensure static/ folder is uploaded

### View Logs:
1. Go to Vercel dashboard
2. Click your project
3. Go to "Functions" tab to see serverless function logs
4. Check for error messages

### Update Code:
1. Make changes to files on GitHub
2. Vercel automatically redeploys on every commit
3. No manual redeployment needed

## Your Deployment URLs

- **GitHub Repository**: `https://github.com/YOUR_USERNAME/ai-resume-analyzer`
- **Live Application**: `https://your-project-name.vercel.app`
- **Vercel Dashboard**: `https://vercel.com/dashboard`

## Key Features Working Live:
✅ AI-powered resume analysis with fallback system  
✅ Gamification with XP, badges, and achievements  
✅ Job matching and compatibility scoring  
✅ File upload (PDF/DOCX support)  
✅ Responsive design for all devices  
✅ PostgreSQL database with Supabase  

Your resume analyzer is now live and accessible worldwide for free!