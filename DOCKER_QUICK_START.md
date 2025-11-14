# 🐳 Docker Deployment - Simple Steps

## Step 1: Install Docker Desktop (One-Time Setup)

### Download Docker Desktop
1. Go to: https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer
4. **Restart your computer** (Required!)

### Verify Installation
After restart, open PowerShell and run:
```powershell
docker --version
docker-compose --version
```

You should see:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

---

## Step 2: Deploy Your System (5 Minutes)

### Open PowerShell
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
```

### Run Deploy Script
```powershell
.\deploy_docker.ps1
```

### What Happens:
```
📦 Building Docker images...       (2 min)
🚀 Starting all services...        (30 sec)
⏳ Waiting for services to start...
🗄️ Initializing databases...      (1 min)
🐾 Populating pets...              (30 sec)
🏥 Populating vet records...       (1 min)
✅ Deployment Complete!
```

---

## Step 3: Access Your Systems

Open your browser:
- **Adoption System**: http://localhost:5000
- **Shelter System**: http://localhost:5001
- **Veterinary System**: http://localhost:5002

---

## 🎯 That's It!

You now have:
- ✅ 3 web services running
- ✅ 20 pets (10 dogs, 10 cats)
- ✅ 20 health records with vaccinations
- ✅ 3 veterinarians
- ✅ 5 appointments
- ✅ Full cross-system integration

---

## 🛑 To Stop Services

```powershell
docker-compose down
```

---

## 🔄 To Restart Services

```powershell
docker-compose up -d
```

---

## 📊 View Logs

```powershell
docker-compose logs -f
```

---

## 🧪 Health Check

```powershell
.\health_check.ps1
```

---

## ❓ Troubleshooting

### "Docker not found"
- Install Docker Desktop from link above
- Restart computer
- Try again

### "Port already in use"
```powershell
# Stop any running Python processes
Get-Process python | Stop-Process -Force

# Then try deploy script again
.\deploy_docker.ps1
```

### "Can't connect to Docker"
- Make sure Docker Desktop is running
- Look for Docker icon in system tray
- Wait 1-2 minutes for Docker to fully start

### Services running but no data
```powershell
# Re-populate data
docker-compose exec shelter-system python populate_pets.py
docker-compose exec veterinary-system python populate_vet_records.py
```

---

## 📋 Quick Command Reference

| Task | Command |
|------|---------|
| Deploy everything | `.\deploy_docker.ps1` |
| Start services | `docker-compose up -d` |
| Stop services | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Check status | `docker-compose ps` |
| Restart | `docker-compose restart` |
| Health check | `.\health_check.ps1` |

---

## 🎬 For Your Presentation

### Before Demo:
```powershell
# 1. Start services (5 min before)
docker-compose up -d

# 2. Verify everything works
.\health_check.ps1

# 3. Open browser tabs
# - http://localhost:5000
# - http://localhost:5001
# - http://localhost:5002
```

### During Demo:
1. Show pet browsing (localhost:5000)
2. Show health records (localhost:5002)
3. Show appointments (localhost:5002)
4. Test APIs with Postman

### After Demo:
```powershell
# Keep running or stop
docker-compose down
```

---

## 🎓 Complete Documentation

For detailed information, see:
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Complete Docker guide
- **[README.md](README.md)** - Project overview
- **[POSTMAN_API_GUIDE.md](POSTMAN_API_GUIDE.md)** - API testing

---

## ✅ Success Checklist

Before your presentation:
- [ ] Docker Desktop installed
- [ ] Deployment script run successfully
- [ ] All 3 systems accessible
- [ ] Health check passed
- [ ] Tested on browser
- [ ] APIs tested in Postman

---

**Need Help?** Check [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for troubleshooting!

**Ready to deploy?** Run: `.\deploy_docker.ps1`
