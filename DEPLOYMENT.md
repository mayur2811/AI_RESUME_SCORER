# Deploying AI Resume Analyzer to Vercel

## Prerequisites

1. A Vercel account (free tier available)
2. A GitHub account to host your code
3. PostgreSQL database (for production)
4. OpenAI API key

## Step 1: Prepare Your Repository

1. Push your code to a GitHub repository
2. Ensure all files are committed:
   - `vercel.json` (deployment configuration)
   - `requirements.txt` (Python dependencies)
   - `api/index.py` (Vercel entry point)

## Step 2: Deploy to Vercel

### Option A: Using Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Configure environment variables (see below)
6. Click "Deploy"

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel

# Follow the prompts and set environment variables
```

## Step 3: Configure Environment Variables

In your Vercel project dashboard, go to Settings > Environment Variables and add:

### Required Variables:
- `DATABASE_URL`: Your PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database`
  - Get from services like Supabase, Railway, or Neon
- `OPENAI_API_KEY`: Your OpenAI API key
- `SESSION_SECRET`: A random secret key for sessions
  - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

### Optional Variables:
- `FLASK_ENV`: Set to `production`

## Step 4: Database Setup

### Option A: Supabase (Recommended - Free tier)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the connection string
5. Use as your `DATABASE_URL`

### Option B: Railway
1. Go to [railway.app](https://railway.app)
2. Create a new PostgreSQL database
3. Copy the connection URL
4. Use as your `DATABASE_URL`

### Option C: Neon
1. Go to [neon.tech](https://neon.tech)
2. Create a new database
3. Copy the connection string
4. Use as your `DATABASE_URL`

## Step 5: Test Your Deployment

1. Wait for deployment to complete
2. Visit your Vercel URL
3. Test file upload and analysis features
4. Check that gamification features work

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **Database connection fails**: Verify `DATABASE_URL` format
3. **OpenAI API fails**: Check `OPENAI_API_KEY` is set correctly
4. **File uploads fail**: Vercel has temporary storage limitations

### File Upload Note:
Vercel functions have temporary storage. Uploaded files are lost after function execution. For production, consider:
- Using cloud storage (AWS S3, Cloudinary)
- Processing files in memory only
- Using Vercel Blob storage

### Logs:
Check deployment logs in Vercel dashboard under Functions tab.

## Production Considerations

1. **Database**: Use a managed PostgreSQL service
2. **File Storage**: Implement cloud storage for uploaded files
3. **Monitoring**: Set up error tracking (Sentry)
4. **Performance**: Enable caching for static assets
5. **Security**: Use strong session secrets and HTTPS

## Custom Domain (Optional)

1. In Vercel dashboard, go to Settings > Domains
2. Add your custom domain
3. Configure DNS as instructed
4. SSL is automatically provided

Your AI Resume Analyzer will be live at: `https://your-project-name.vercel.app`