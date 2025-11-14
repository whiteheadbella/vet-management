# 🚀 Deployment Guide - Pet Adoption System

Complete guide to deploy your Pet Adoption System for project presentations.

## 📋 Table of Contents
1. [Quick Deploy Options](#quick-deploy-options)
2. [Render.com Deployment (Recommended)](#rendercom-deployment-recommended)
3. [Docker Deployment](#docker-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Railway.app Deployment](#railwayapp-deployment)
6. [Python Anywhere Deployment](#python-anywhere-deployment)
7. [Local Network Deployment](#local-network-deployment)

---

## 🎯 Quick Deploy Options

### Best for Project Presentation:

| Platform | Difficulty | Cost | Multi-Service Support | Recommended |
|----------|-----------|------|----------------------|-------------|
| **Render.com** | ⭐ Easy | Free | ✅ Yes | ⭐⭐⭐⭐⭐ |
| **Railway.app** | ⭐ Easy | Free | ✅ Yes | ⭐⭐⭐⭐ |
| **Docker** | ⭐⭐ Medium | Free | ✅ Yes | ⭐⭐⭐⭐ |
| **Heroku** | ⭐⭐ Medium | Paid | ⚠️ Limited | ⭐⭐⭐ |
| **Python Anywhere** | ⭐⭐ Medium | Free | ❌ No | ⭐⭐ |

---

## 🌟 Render.com Deployment (RECOMMENDED)

**Best for:** Project presentations, free hosting, easy setup

### Step 1: Prepare Your Repository

1. **Create GitHub Repository**
```bash
cd C:\Users\white\OneDrive\Desktop\Vet-Management
git init
git add .
git commit -m "Initial commit - Pet Adoption System"
```

2. **Push to GitHub**
```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/pet-adoption-system.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render.com

1. **Sign up at [render.com](https://render.com)** (Free account)

2. **Connect GitHub**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Services**
   - Render will create 3 web services automatically:
     - `pet-adoption-system` (Port 5000)
     - `pet-shelter-system` (Port 5001)
     - `pet-veterinary-system` (Port 5002)

4. **Set Environment Variables** (if needed)
   - Go to each service → Environment
   - Add any custom variables from `.env.example`

5. **Deploy**
   - Click "Apply"
   - Wait 5-10 minutes for deployment
   - You'll get URLs like:
     - `https://pet-adoption-system.onrender.com`
     - `https://pet-shelter-system.onrender.com`
     - `https://pet-veterinary-system.onrender.com`

### Step 3: Update System URLs

After deployment, update the environment variables with actual URLs:

```bash
# In Render.com dashboard, update each service:
ADOPTION_SYSTEM_URL=https://pet-adoption-system.onrender.com
SHELTER_SYSTEM_URL=https://pet-shelter-system.onrender.com
VETERINARY_SYSTEM_URL=https://pet-veterinary-system.onrender.com
```

### Step 4: Initialize Database

Render will automatically run these commands during build:
- `python init_databases.py` - Creates database tables
- `python populate_pets.py` - Adds 20 pets
- `python populate_vet_records.py` - Adds health records

**Your system is now live!** 🎉

---

## 🐳 Docker Deployment

**Best for:** Local presentations, testing, full control

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Install [Docker Compose](https://docs.docker.com/compose/install/)

### Step 1: Build and Run

```bash
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 2: Initialize Data

```bash
# Initialize databases
docker-compose exec adoption-system python init_databases.py

# Populate pets
docker-compose exec shelter-system python populate_pets.py

# Populate vet records
docker-compose exec veterinary-system python populate_vet_records.py
```

### Step 3: Access Services

- **Adoption System**: http://localhost:5000
- **Shelter System**: http://localhost:5001
- **Veterinary System**: http://localhost:5002

### Useful Docker Commands

```bash
# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View running containers
docker-compose ps

# View logs for specific service
docker-compose logs adoption-system

# Remove all containers and volumes
docker-compose down -v
```

---

## 🚂 Railway.app Deployment

**Best for:** Quick deployment, automatic HTTPS, free tier

### Step 1: Install Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Or use PowerShell:
iwr https://railway.app/install.ps1 | iex
```

### Step 2: Login and Initialize

```bash
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Login to Railway
railway login

# Create new project
railway init

# Link to project
railway link
```

### Step 3: Deploy Each Service

```bash
# Deploy Adoption System
railway up adoption_system/app.py --name pet-adoption

# Deploy Shelter System
railway up shelter_system/app.py --name pet-shelter

# Deploy Veterinary System
railway up veterinary_system/app.py --name pet-veterinary
```

### Step 4: Set Environment Variables

```bash
# Set variables for each service
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=$(openssl rand -hex 32)
```

### Step 5: Get URLs

```bash
# Get service URLs
railway domain
```

Railway will provide URLs like:
- `https://pet-adoption-production.up.railway.app`
- `https://pet-shelter-production.up.railway.app`
- `https://pet-veterinary-production.up.railway.app`

---

## 🟣 Heroku Deployment

**Note:** Heroku no longer offers free tier, but suitable for paid presentations

### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Create Heroku Apps

```bash
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Login
heroku login

# Create three apps
heroku create pet-adoption-system
heroku create pet-shelter-system
heroku create pet-veterinary-system
```

### Step 3: Deploy Adoption System

```bash
# Add Git remote
git remote add heroku-adoption https://git.heroku.com/pet-adoption-system.git

# Set buildpack
heroku buildpacks:set heroku/python -a pet-adoption-system

# Deploy
git push heroku-adoption main

# Scale dyno
heroku ps:scale web=1 -a pet-adoption-system
```

### Step 4: Set Environment Variables

```bash
heroku config:set FLASK_ENV=production -a pet-adoption-system
heroku config:set SECRET_KEY=$(openssl rand -hex 32) -a pet-adoption-system
heroku config:set SHELTER_SYSTEM_URL=https://pet-shelter-system.herokuapp.com -a pet-adoption-system
heroku config:set VETERINARY_SYSTEM_URL=https://pet-veterinary-system.herokuapp.com -a pet-adoption-system
```

### Step 5: Initialize Database

```bash
heroku run python init_databases.py -a pet-adoption-system
heroku run python populate_pets.py -a pet-shelter-system
heroku run python populate_vet_records.py -a pet-veterinary-system
```

---

## 🐍 Python Anywhere Deployment

**Best for:** Simple Python apps (Note: Supports only 1 service on free tier)

### Step 1: Sign Up

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create free account

### Step 2: Upload Files

```bash
# Option 1: Upload via web interface
# Go to Files → Upload files

# Option 2: Clone from GitHub
# Open Bash console and run:
git clone https://github.com/YOUR_USERNAME/pet-adoption-system.git
```

### Step 3: Setup Virtual Environment

```bash
cd pet-adoption-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to Web tab
2. Click "Add a new web app"
3. Select "Manual configuration"
4. Python 3.10
5. Set source code: `/home/YOUR_USERNAME/pet-adoption-system`
6. Set WSGI file to point to `adoption_system/app.py`

### Step 5: Edit WSGI Configuration

```python
import sys
import os

path = '/home/YOUR_USERNAME/pet-adoption-system'
if path not in sys.path:
    sys.path.append(path)

from adoption_system.app import app as application
```

### Step 6: Reload Web App

Click "Reload" button - Your app will be live at:
`https://YOUR_USERNAME.pythonanywhere.com`

**Note:** Free tier only supports 1 web app, so you'd need to deploy all 3 systems on separate accounts or upgrade to paid plan.

---

## 🏠 Local Network Deployment

**Best for:** In-person presentations, demos without internet

### Step 1: Find Your Local IP

```powershell
# Windows PowerShell
ipconfig

# Look for "IPv4 Address" under your active network
# Example: 192.168.1.100
```

### Step 2: Update Configuration

Edit `config.py`:
```python
# Replace localhost with your IP
ADOPTION_SYSTEM_URL = 'http://192.168.1.100:5000'
SHELTER_SYSTEM_URL = 'http://192.168.1.100:5001'
VETERINARY_SYSTEM_URL = 'http://192.168.1.100:5002'
```

### Step 3: Configure Firewall

```powershell
# Allow incoming connections on ports 5000-5002
New-NetFirewallRule -DisplayName "Pet Adoption System" -Direction Inbound -LocalPort 5000-5002 -Protocol TCP -Action Allow
```

### Step 4: Run with Host Binding

```bash
# Terminal 1
python adoption_system/app.py --host=0.0.0.0 --port=5000

# Terminal 2
python shelter_system/app.py --host=0.0.0.0 --port=5001

# Terminal 3
python veterinary_system/app.py --host=0.0.0.0 --port=5002
```

Or modify each `app.py` to bind to `0.0.0.0`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 5: Access from Other Devices

Anyone on your network can access:
- **Adoption System**: http://192.168.1.100:5000
- **Shelter System**: http://192.168.1.100:5001
- **Veterinary System**: http://192.168.1.100:5002

---

## 🔧 Production Configurations

### Update Flask Apps for Production

Add to each `app.py`:

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### Environment Variables for Production

Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=super-secret-key-change-this
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ADOPTION_SYSTEM_URL=https://your-adoption-url.com
SHELTER_SYSTEM_URL=https://your-shelter-url.com
VETERINARY_SYSTEM_URL=https://your-veterinary-url.com
```

### Database Migration to PostgreSQL

For production, use PostgreSQL instead of SQLite:

```python
# config.py
import os

class Config:
    if os.environ.get('DATABASE_URL'):
        # Production - PostgreSQL
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Development - SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///adoption_system.db'
```

---

## 📱 QR Code for Easy Access

Generate QR codes for your deployed URLs:

```python
# install: pip install qrcode[pil]
import qrcode

url = "https://pet-adoption-system.onrender.com"
qr = qrcode.make(url)
qr.save("adoption_system_qr.png")
```

Or use online generator: https://www.qr-code-generator.com/

---

## ✅ Pre-Presentation Checklist

Before your presentation, verify:

- [ ] All 3 services are running and accessible
- [ ] Database is populated with sample data (20 pets, 20 health records)
- [ ] Cross-system integration works (test in Postman)
- [ ] Test adoption workflow end-to-end
- [ ] Test appointment scheduling
- [ ] Test health records viewing
- [ ] All images load correctly
- [ ] Mobile responsiveness works
- [ ] Create QR codes for easy access
- [ ] Test on different devices (phone, tablet, laptop)
- [ ] Prepare backup (local Docker deployment)

---

## 🐛 Troubleshooting

### Issue: Services Can't Communicate

**Solution:** Update CORS settings in each `extensions.py`:
```python
from flask_cors import CORS

cors = CORS(resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Issue: Database Not Initialized

**Solution:** Run initialization commands:
```bash
python init_databases.py
python populate_pets.py
python populate_vet_records.py
```

### Issue: Port Already in Use

**Solution:** Kill process on port:
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Issue: Module Import Errors

**Solution:** Set PYTHONPATH:
```bash
set PYTHONPATH=C:\Users\white\OneDrive\Desktop\Vet-Management
```

---

## 🎬 Demo Script for Presentation

### 1. Introduction (2 min)
"Today I'll demonstrate a comprehensive Pet Adoption System with three integrated microservices..."

### 2. System Architecture (3 min)
- Show architecture diagram
- Explain three systems and their roles
- Show API integration using Postman

### 3. Live Demo (10 min)
1. **Browse Pets** (Adoption System)
   - Navigate to adoption system URL
   - Filter by species, breed
   - Show pet cards with images

2. **View Pet Details** (Shelter System)
   - Click on a pet
   - Show detailed information
   - Display characteristics

3. **View Health Records** (Veterinary System)
   - Navigate to veterinary system
   - Show vaccination history
   - Display complete health profile

4. **Schedule Appointment** (Integration)
   - Schedule a vet appointment
   - Show cross-system communication

5. **Complete Adoption** (Full Workflow)
   - Submit adoption application
   - Update pet status
   - Demonstrate full integration

### 4. Technical Highlights (3 min)
- RESTful API design
- Microservices architecture
- Database schema
- External API integration (Dog/Cat APIs)

### 5. Q&A (2 min)

---

## 🌐 Recommended: Render.com Quick Start

**Fastest deployment for presentation:**

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Pet Adoption System"
git remote add origin https://github.com/YOUR_USERNAME/pet-adoption-system.git
git push -u origin main

# 2. Go to render.com and sign in
# 3. Click "New +" → "Blueprint"
# 4. Connect repository
# 5. Click "Apply"
# 6. Wait 10 minutes
# 7. Done! You'll have 3 live URLs
```

**Total time: 15 minutes** ⏱️

---

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 512 MB per service
- **Storage**: 100 MB
- **Bandwidth**: 1 GB/month (free tier)

### Recommended for Presentation
- **RAM**: 1 GB per service
- **Storage**: 500 MB
- **Bandwidth**: 10 GB/month
- **HTTPS**: Enabled (for secure demo)

---

## 🎓 Best Practices for Presentation

1. **Test Before Presentation**
   - Run through demo 2-3 times
   - Test on different networks
   - Have backup deployment ready

2. **Prepare Screenshots**
   - In case of network issues
   - Show complex workflows
   - Highlight key features

3. **Use QR Codes**
   - For easy audience access
   - Print on handouts
   - Display on slides

4. **Monitor Performance**
   - Check service status before presentation
   - Monitor response times
   - Have local backup running

5. **Prepare for Questions**
   - Know your tech stack
   - Understand integration points
   - Be ready to show code

---

## 🎉 Success!

Your Pet Adoption System is now deployed and ready for presentation!

**Quick Links:**
- 📖 [Full Documentation](README.md)
- 🔌 [API Guide](POSTMAN_API_GUIDE.md)
- 🐳 [Docker Guide](https://docs.docker.com/)
- 🌐 [Render.com Docs](https://render.com/docs)

**Need Help?**
- Check troubleshooting section above
- Review deployment logs
- Test with Postman collection

Good luck with your presentation! 🚀
