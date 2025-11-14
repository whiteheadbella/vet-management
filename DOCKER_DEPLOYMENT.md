# 🐳 Docker Deployment Guide - Pet Adoption System

Complete guide to deploy all three systems using Docker in just 5 minutes!

---

## 📋 Prerequisites

### Install Docker Desktop

**Windows:**
1. Download: https://www.docker.com/products/docker-desktop
2. Run installer
3. Restart computer
4. Open Docker Desktop and wait for it to start

**Verify Installation:**
```powershell
docker --version
docker-compose --version
```

You should see versions like:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

---

## 🚀 Quick Deploy (5 Minutes)

### Method 1: Using Deploy Script (Easiest)

**Step 1:** Open PowerShell in your project folder
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
```

**Step 2:** Run the deploy script
```powershell
.\deploy_docker.ps1
```

**That's it!** The script will:
- ✅ Build 3 Docker containers
- ✅ Start all services
- ✅ Initialize databases
- ✅ Populate with 20 pets
- ✅ Add 20 health records
- ✅ Create 3 vets
- ✅ Schedule 5 appointments

**Wait 5 minutes** and access:
- **Adoption System**: http://localhost:5000
- **Shelter System**: http://localhost:5001
- **Veterinary System**: http://localhost:5002

---

### Method 2: Manual Docker Commands

If you prefer to run commands manually:

**Step 1: Build Images**
```powershell
docker-compose build
```

**Step 2: Start Services**
```powershell
docker-compose up -d
```

**Step 3: Wait for Services to Start**
```powershell
Start-Sleep -Seconds 10
```

**Step 4: Initialize Databases**
```powershell
docker-compose exec adoption-system python init_databases.py
```

**Step 5: Populate Data**
```powershell
docker-compose exec shelter-system python populate_pets.py
docker-compose exec veterinary-system python populate_vet_records.py
```

**Done!** Access at http://localhost:5000-5002

---

## 🏗️ Docker Architecture

```
┌────────────────────────────────────────────────────┐
│              Docker Environment                     │
├────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │     pet-adoption-network (Bridge)            │ │
│  │                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐        │ │
│  │  │  Container 1 │  │  Container 2 │        │ │
│  │  │              │  │              │        │ │
│  │  │  Adoption    │  │   Shelter    │        │ │
│  │  │   System     │  │   System     │        │ │
│  │  │              │  │              │        │ │
│  │  │  Port: 5000  │  │  Port: 5001  │        │ │
│  │  └──────────────┘  └──────────────┘        │ │
│  │                                              │ │
│  │  ┌──────────────┐                           │ │
│  │  │  Container 3 │                           │ │
│  │  │              │                           │ │
│  │  │ Veterinary   │                           │ │
│  │  │   System     │                           │ │
│  │  │              │                           │ │
│  │  │  Port: 5002  │                           │ │
│  │  └──────────────┘                           │ │
│  │                                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
│  Shared Volumes:                                   │
│  • adoption_system.db                              │
│  • shelter_system.db                               │
│  • veterinary_system.db                            │
│  • static/uploads                                  │
│                                                     │
└────────────────────────────────────────────────────┘
           │
           ▼
   http://localhost:5000-5002
```

---

## 📦 What Gets Deployed

### Containers:
1. **adoption-system** (Port 5000)
   - User management
   - Pet browsing
   - Adoption applications

2. **shelter-system** (Port 5001)
   - Pet inventory
   - Pet images
   - REST API

3. **veterinary-system** (Port 5002)
   - Health records
   - Appointments
   - Vaccinations

### Pre-populated Data:
- 🐕 10 Dogs (Various breeds)
- 🐈 10 Cats (Various breeds)
- 🏥 20 Complete health records
- 👨‍⚕️ 3 Veterinarians
- 📅 5 Scheduled appointments

---

## 🔧 Docker Commands Reference

### Start Services
```powershell
# Start all containers
docker-compose up -d

# Start and view logs
docker-compose up

# Start specific service
docker-compose up adoption-system
```

### Stop Services
```powershell
# Stop all containers
docker-compose down

# Stop and remove volumes (delete data)
docker-compose down -v
```

### View Logs
```powershell
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs adoption-system
docker-compose logs shelter-system
docker-compose logs veterinary-system

# Last 50 lines
docker-compose logs --tail=50
```

### Check Container Status
```powershell
# List running containers
docker-compose ps

# Detailed container info
docker ps

# Check resource usage
docker stats
```

### Restart Services
```powershell
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart adoption-system
```

### Execute Commands in Containers
```powershell
# Open shell in container
docker-compose exec adoption-system /bin/bash

# Run Python command
docker-compose exec adoption-system python -c "print('Hello')"

# Re-populate data
docker-compose exec shelter-system python populate_pets.py
```

### Clean Up
```powershell
# Remove stopped containers
docker-compose rm

# Remove all containers and networks
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove unused Docker resources
docker system prune -a
```

---

## 🧪 Testing Your Deployment

### Test 1: Check Services Are Running
```powershell
docker-compose ps
```

You should see 3 containers with status "Up":
```
NAME                          STATUS
adoption-system               Up 2 minutes
shelter-system                Up 2 minutes
veterinary-system             Up 2 minutes
```

### Test 2: Check Web Access
Open browser and visit:
- http://localhost:5000 - Should show Adoption System
- http://localhost:5001 - Should show Shelter System
- http://localhost:5002 - Should show Veterinary System

### Test 3: Check APIs
```powershell
# Test Shelter API - Get pets
curl http://localhost:5001/api/pets/

# Test Veterinary API - Get vets
curl http://localhost:5002/api/vets

# Test Health API - Get health record
curl http://localhost:5002/api/health/1
```

### Test 4: Run Health Check
```powershell
.\health_check.ps1
```

---

## 🔍 Troubleshooting

### Problem: "docker-compose: command not found"

**Solution:** Docker Desktop not installed or not running
```powershell
# Check if Docker Desktop is running
docker --version

# If not installed, download from:
# https://www.docker.com/products/docker-desktop
```

---

### Problem: "Port is already allocated"

**Solution:** Another process is using ports 5000-5002
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess

# Kill the process (replace <PID> with actual process ID)
Stop-Process -Id <PID> -Force

# Or stop all Python processes
Get-Process python | Stop-Process -Force
```

---

### Problem: "Cannot connect to Docker daemon"

**Solution:** Docker Desktop is not running
```powershell
# Start Docker Desktop from Start Menu
# Wait 1-2 minutes for it to fully start
# Then try again
```

---

### Problem: Containers start but show errors in logs

**Solution:** Check logs and restart
```powershell
# View error logs
docker-compose logs

# Restart services
docker-compose restart

# Or rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### Problem: "No data showing in application"

**Solution:** Re-populate databases
```powershell
# Re-run population scripts
docker-compose exec shelter-system python populate_pets.py
docker-compose exec veterinary-system python populate_vet_records.py
```

---

### Problem: Changes to code not reflecting

**Solution:** Rebuild containers
```powershell
# Stop containers
docker-compose down

# Rebuild images
docker-compose build

# Start again
docker-compose up -d
```

---

### Problem: "exec: python: executable file not found"

**Solution:** Container build issue
```powershell
# Rebuild without cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 💡 Development Tips

### Live Code Editing

To enable live code reload without rebuilding:

**Option 1: Mount volumes** (Add to docker-compose.yml)
```yaml
volumes:
  - ./adoption_system:/app/adoption_system
  - ./shelter_system:/app/shelter_system
  - ./veterinary_system:/app/veterinary_system
```

**Option 2: Use development mode**
```powershell
# Set Flask environment to development
$env:FLASK_ENV="development"
docker-compose up
```

### Viewing Databases

```powershell
# Access SQLite database
docker-compose exec adoption-system sqlite3 adoption_system.db

# Run SQL query
docker-compose exec adoption-system sqlite3 adoption_system.db "SELECT * FROM users;"
```

### Port Mapping

To change ports, edit `docker-compose.yml`:
```yaml
ports:
  - "8000:5000"  # Access at localhost:8000 instead of 5000
```

---

## 🎬 Demo Workflow

### Before Presentation

**1. Start Services (5 minutes before)**
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
docker-compose up -d
```

**2. Verify Everything Works**
```powershell
.\health_check.ps1
```

**3. Open Browser Tabs**
- http://localhost:5000 (Adoption)
- http://localhost:5001 (Shelter)
- http://localhost:5002 (Veterinary)

### During Presentation

**Demo Flow:**
1. **Browse Pets** (localhost:5000)
   - Show 20 pets with images
   - Filter by species

2. **View Health Records** (localhost:5002)
   - Browse health records
   - Show vaccination history

3. **Manage Appointments** (localhost:5002)
   - View appointments
   - Schedule new appointment

4. **API Testing** (Postman)
   - Show cross-system integration
   - Test API endpoints

### After Presentation

```powershell
# Stop services
docker-compose down

# Or keep running for demos
docker-compose ps
```

---

## 📊 Resource Usage

### Typical Docker Resource Requirements:

```
Per Container:
- CPU: ~10-20%
- RAM: ~100-200 MB
- Disk: ~300 MB

Total for 3 containers:
- CPU: ~30-60%
- RAM: ~300-600 MB
- Disk: ~1 GB
```

### Monitor Resources:
```powershell
# Real-time monitoring
docker stats

# Container resource limits
docker-compose config
```

---

## 🔒 Production Considerations

For production deployment, update `docker-compose.yml`:

### Security:
```yaml
environment:
  - FLASK_ENV=production
  - DEBUG=False
  - SECRET_KEY=${SECRET_KEY}
```

### Use PostgreSQL:
```yaml
services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
```

### Use Gunicorn:
```yaml
command: gunicorn adoption_system.app:app --bind 0.0.0.0:5000 --workers 4
```

---

## ✅ Quick Reference

### Essential Commands:
```powershell
# Deploy everything
.\deploy_docker.ps1

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart service
docker-compose restart adoption-system

# Clean everything
docker-compose down -v
```

### URLs:
- Adoption: http://localhost:5000
- Shelter: http://localhost:5001
- Veterinary: http://localhost:5002

### Data Location:
- Databases: `./adoption_system.db`, `./shelter_system.db`, `./veterinary_system.db`
- Uploads: `./static/uploads/`
- Logs: `docker-compose logs`

---

## 🎉 You're Ready!

Your Docker deployment is configured and ready to use!

**Quick Start:**
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
.\deploy_docker.ps1
```

**Wait 5 minutes, then open:** http://localhost:5000

**Need help?** Check troubleshooting section above or view logs with `docker-compose logs`

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask + Docker Best Practices](https://flask.palletsprojects.com/en/3.0.x/deploying/)

**Happy Dockerizing! 🐳**
