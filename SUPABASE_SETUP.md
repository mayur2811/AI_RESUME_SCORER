# Supabase Setup Guide

## Your Supabase Project Configuration

**Project Details:**
- Project URL: `https://vdhotrhbvlcntplhsagy.supabase.co`
- Project ID: `vdhotrhbvlcntplhsagy`  
- API Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkaG90cmhidmxjbnRwbGhzYWd5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4NTkxMjEsImV4cCI6MjA2ODQzNTEyMX0.x1uEbziEAQkvBFdtFCOvOJoUGOhUbK9uta7WVPRD0K4`
- Database Password: `Mayur@28112002`

## Getting the Correct Database URL

### Step 1: Access Database Settings
1. Go to your Supabase dashboard: https://supabase.com/dashboard/projects
2. Select your project: `vdhotrhbvlcntplhsagy`
3. Click **Settings** (gear icon in sidebar)
4. Click **Database**

### Step 2: Find Connection String
Look for one of these sections:
- **"Connection string"**
- **"Database URL"** 
- **"Connection pooling"**

### Step 3: Copy the Correct Format
The connection string should be one of these formats:

**Direct Connection (Port 5432):**
```
postgresql://postgres:[YOUR-PASSWORD]@db.vdhotrhbvlcntplhsagy.supabase.co:5432/postgres
```

**Connection Pooling (Port 6543):**
```
postgresql://postgres.vdhotrhbvlcntplhsagy:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### Step 4: Replace Password
Replace `[YOUR-PASSWORD]` with: `Mayur@28112002`

**Important:** URL encode special characters:
- `@` becomes `%40`  
- So `Mayur@28112002` becomes `Mayur%4028112002`

## Final Connection Strings to Try

**Option 1 (Direct):**
```
postgresql://postgres:Mayur%4028112002@db.vdhotrhbvlcntplhsagy.supabase.co:5432/postgres
```

**Option 2 (Pooled):**
```
postgresql://postgres.vdhotrhbvlcntplhsagy:Mayur%4028112002@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

## For Local Development
Update your `.env` file:
```env
DATABASE_URL=postgresql://[CORRECT_CONNECTION_STRING]
SUPABASE_URL=https://vdhotrhbvlcntplhsagy.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkaG90cmhidmxjbnRwbGhzYWd5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4NTkxMjEsImV4cCI6MjA2ODQzNTEyMX0.x1uEbziEAQkvBFdtFCOvOJoUGOhUbK9uta7WVPRD0K4
SESSION_SECRET=your-random-secret-key
```

## For Vercel Deployment
Set these environment variables in your Vercel project:

- `DATABASE_URL`: [CORRECT_CONNECTION_STRING]
- `OPENAI_API_KEY`: [Your OpenAI API key]  
- `SESSION_SECRET`: [Random secret key]

## Troubleshooting

### Common Issues:
1. **"Name or service not known"** - Wrong hostname format
2. **"Tenant or user not found"** - Incorrect username format
3. **"Authentication failed"** - Wrong password or encoding

### Solution:
Copy the **exact** connection string from your Supabase dashboard and only replace the password portion.

## Testing Connection
Run this command to test:
```bash
python -c "
from sqlalchemy import create_engine, text
DATABASE_URL = 'your-connection-string-here'
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('✅ Connection successful!')
"
```

## Next Steps
1. Find the correct connection string in your Supabase dashboard
2. Test the connection locally
3. Update your deployment configuration
4. Deploy to Vercel with the working connection string