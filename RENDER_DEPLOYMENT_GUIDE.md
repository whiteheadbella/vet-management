# 🚀 Complete Render.com Deployment Guide

## Prerequisites
- GitHub account
- Render.com account (sign up at https://render.com)
- Git installed on your computer

---

## Step 1: Prepare Your Project for GitHub

### 1.1 Create .gitignore file (if not exists)
```bash
# Already done - your project has .gitignore
```

### 1.2 Initialize Git and Push to GitHub
```powershell
# Navigate to project directory
cd c:\Users\white\OneDrive\Desktop\Vet-Management

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Pet Adoption Management System - Ready for Render deployment"

# Create a new repository on GitHub:
# Go to https://github.com/new
# Repository name: vet-management
# Description: Pet Adoption Management System
# Public or Private (your choice)
# Do NOT add README, .gitignore, or license (we have them)

# Link your local repo to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/vet-management.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Sign Up for Render.com

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (recommended) or email
4. Authorize Render to access your GitHub repositories

---

## Step 3: Deploy Adoption System (Port 5000)

### 3.1 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your `vet-management` repository
3. Configure:

```yaml
Name: pet-adoption-system
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python adoption_system/app.py
```

### 3.2 Set Environment Variables
Click "Advanced" → Add Environment Variables:

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
SHELTER_SYSTEM_URL=https://shelter-system.onrender.com
VETERINARY_SYSTEM_URL=https://veterinary-system.onrender.com
```

### 3.3 Select Plan
- Choose: **Free** (0$/month, 750 hours)
- Click "Create Web Service"

**Note the URL:** `https://pet-adoption-system.onrender.com`

---

## Step 4: Deploy Shelter System (Port 5001)

### 4.1 Create Another Web Service
1. Dashboard → "New +" → "Web Service"
2. Select `vet-management` repository again
3. Configure:

```yaml
Name: shelter-system
Region: Same as adoption system
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python shelter_system/app.py
```

### 4.2 Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
ADOPTION_SYSTEM_URL=https://pet-adoption-system.onrender.com
VETERINARY_SYSTEM_URL=https://veterinary-system.onrender.com
```

### 4.3 Select Free Plan → Create

**Note the URL:** `https://shelter-system.onrender.com`

---

## Step 5: Deploy Veterinary System (Port 5002)

### 5.1 Create Third Web Service
1. Dashboard → "New +" → "Web Service"
2. Select `vet-management` repository
3. Configure:

```yaml
Name: veterinary-system
Region: Same as others
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python veterinary_system/app.py
```

### 5.2 Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
ADOPTION_SYSTEM_URL=https://pet-adoption-system.onrender.com
SHELTER_SYSTEM_URL=https://shelter-system.onrender.com
```

### 5.3 Select Free Plan → Create

**Note the URL:** `https://veterinary-system.onrender.com`

---

## Step 6: Update API URLs in Code

After all services are deployed, update `config.py`:

```python
# System URLs (UPDATE WITH YOUR ACTUAL RENDER URLS)
ADOPTION_SYSTEM_URL = os.getenv('ADOPTION_SYSTEM_URL', 'https://pet-adoption-system.onrender.com')
SHELTER_SYSTEM_URL = os.getenv('SHELTER_SYSTEM_URL', 'https://shelter-system.onrender.com')
VETERINARY_SYSTEM_URL = os.getenv('VETERINARY_SYSTEM_URL', 'https://veterinary-system.onrender.com')
```

Commit and push:
```bash
git add config.py
git commit -m "Update URLs for Render deployment"
git push
```

Render will **auto-deploy** when you push!

---

## Step 7: Initialize Databases (Important!)

Each service needs its database initialized. For each service:

1. Go to Render Dashboard
2. Click on service (e.g., "pet-adoption-system")
3. Go to "Shell" tab
4. Run:

```bash
# For Adoption System
python -c "from adoption_system.app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

# For Shelter System
python -c "from shelter_system.app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

# For Veterinary System
python -c "from veterinary_system.app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

Or run the initialization scripts:
```bash
python init_databases.py
python populate_pets.py
```

---

## Step 8: Test Your Deployment

### 8.1 Check Service Status
- All 3 services should show "Live" with green dot
- Check logs for any errors

### 8.2 Access Your Systems
```
Adoption System:   https://pet-adoption-system.onrender.com
Shelter System:    https://shelter-system.onrender.com
Veterinary System: https://veterinary-system.onrender.com
```

### 8.3 Test Integration
1. Open Adoption System
2. Browse Pets (should fetch from Shelter API)
3. View pet details (should show health records from Vet API)

---

## Step 9: Upgrade Database (Optional - Recommended)

**Important:** Free tier SQLite doesn't persist between restarts!

### Solution: Add PostgreSQL (Free 256MB)

For each service:
1. Go to service dashboard
2. Click "New +" → "PostgreSQL"
3. Name: `pet-adoption-db` / `shelter-db` / `vet-db`
4. Select Free plan → Create
5. Copy the Internal Database URL
6. Add to service Environment Variables:
   ```
   DATABASE_URL=<your-postgres-url>
   ```

Update `config.py`:
```python
# Database Configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///adoption_system.db')
```

---

## Step 10: Configure Custom Domain (Optional)

### 10.1 Add Custom Domain
1. Go to service → Settings → Custom Domains
2. Add your domain (e.g., `adopt.yourdomain.com`)
3. Update DNS records as instructed
4. Render provides free SSL certificates!

---

## 🎯 Quick Commands Cheat Sheet

### Update and Deploy
```bash
# Make changes
git add .
git commit -m "Your changes"
git push

# Render auto-deploys in ~2 minutes
```

### View Logs
```bash
# In Render Dashboard → Service → Logs tab
# Or use Render CLI:
render logs pet-adoption-system
```

### Manual Deploy
```bash
# In Render Dashboard → Service → Manual Deploy → Deploy latest commit
```

---

## 🔧 Troubleshooting

### Issue: Service not starting
**Solution:** Check logs for errors. Common issues:
- Missing dependencies in `requirements.txt`
- Wrong start command
- Database not initialized

### Issue: API calls failing between services
**Solution:** Check environment variables have correct URLs

### Issue: Database resets on restart (Free tier)
**Solution:** Upgrade to PostgreSQL (also free but persistent)

### Issue: Slow first load (Cold start)
**Solution:** Free tier services sleep after 15 min inactivity. First request wakes them up (~30 seconds)

---

## 📊 Monitoring & Maintenance

### Check Service Health
- Dashboard shows uptime, response time, memory usage
- Set up notifications for downtime

### Update Dependencies
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### View Database
Use Render Shell:
```bash
# Access database
sqlite3 shelter_system.db
# Or for PostgreSQL
psql $DATABASE_URL
```

---

## 💰 Cost Breakdown

### Free Tier Limits (Per Service)
- ✅ 750 hours/month (enough for 1 service running 24/7)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ 100 GB bandwidth/month
- ⚠️ Services sleep after 15 min inactivity
- ⚠️ SQLite not persistent

### To Keep All 3 Running 24/7
- Need 3 × 750 hours = 2,250 hours/month
- But free tier gives 750 hours total
- **Solution:** Upgrade to Starter ($7/month per service) or use PostgreSQL + keep services active

---

## 🎉 You're Done!

Your Pet Adoption System is now live on the internet!

Share these URLs with your team:
```
🐾 Adoption:  https://pet-adoption-system.onrender.com
🏠 Shelter:   https://shelter-system.onrender.com
🏥 Vet:       https://veterinary-system.onrender.com
```

---

## 🔄 Next Steps

1. ✅ Add custom domain
2. ✅ Upgrade to PostgreSQL for persistent data
3. ✅ Set up monitoring/alerts
4. ✅ Configure backup strategy
5. ✅ Add environment-specific configs (dev/staging/prod)

Need help? Check Render docs: https://render.com/docs
