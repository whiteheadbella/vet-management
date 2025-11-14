# 🚀 Quick Start - Deploy in 5 Minutes!

Choose your deployment method:

## Option 1: Docker (Easiest - Recommended for Local Demo)

**Prerequisites:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

```powershell
# Just run this command:
.\deploy_docker.ps1
```

✅ **Done!** Access at:
- http://localhost:5000 (Adoption System)
- http://localhost:5001 (Shelter System)
- http://localhost:5002 (Veterinary System)

---

## Option 2: Render.com (Best for Online Presentation)

**Prerequisites:** GitHub account + Render.com account (both free)

```powershell
# Run this command and follow prompts:
.\deploy_render.ps1
```

Steps:
1. Script will push code to GitHub
2. Go to [render.com](https://render.com) and connect your repo
3. Click "Apply" - wait 10 minutes
4. Get 3 live URLs with HTTPS!

✅ **Done!** Your system is live on the internet!

---

## Option 3: Local Network (For In-Person Presentation)

```powershell
# Run this command:
.\deploy_local.ps1
```

✅ **Done!** Anyone on your WiFi can access via your IP address!

---

## 📱 For Your Presentation

### Test Your Deployment

```powershell
# Test Shelter API
curl http://localhost:5001/api/pets/

# Test Veterinary API
curl http://localhost:5002/api/health/1

# Test Vets API
curl http://localhost:5002/api/vets
```

### Create QR Codes

Generate QR codes for easy mobile access:
1. Go to https://www.qr-code-generator.com/
2. Enter your deployment URL
3. Download and print

### Demo Checklist

Before your presentation:
- [ ] All 3 services are running
- [ ] Can browse pets with images
- [ ] Can view health records
- [ ] Can view veterinarians
- [ ] Can schedule appointments
- [ ] Test on mobile device
- [ ] Have QR codes ready
- [ ] Backup deployment ready

---

## 🆘 Troubleshooting

### Docker not starting?
```powershell
# Check Docker is running
docker --version

# Restart Docker Desktop
```

### Port already in use?
```powershell
# Kill process on port 5000
$process = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id $process -Force
```

### Can't access from other devices?
```powershell
# Check firewall - run as Administrator
New-NetFirewallRule -DisplayName "Pet Adoption" -Direction Inbound -LocalPort 5000-5002 -Protocol TCP -Action Allow
```

---

## 📊 What Gets Deployed

### Databases
- ✅ 20 dogs with realistic breeds and characteristics
- ✅ 10 cats with realistic breeds and characteristics
- ✅ 20 complete health records with vaccinations
- ✅ 3 veterinarians
- ✅ 5 scheduled appointments

### Features
- ✅ Pet browsing with filters
- ✅ Health record viewing
- ✅ Appointment scheduling
- ✅ Veterinarian profiles
- ✅ Cross-system integration
- ✅ RESTful APIs
- ✅ Responsive design

---

## 🎬 5-Minute Demo Script

1. **Browse Pets** (1 min)
   - Show shelter with 20 pets
   - Filter by dog/cat
   - Show pet images from APIs

2. **View Health Records** (1 min)
   - Navigate to veterinary system
   - View detailed health record
   - Show vaccination history table

3. **Manage Appointments** (1 min)
   - Schedule new appointment
   - View appointment list
   - Show appointment details

4. **View Veterinarians** (1 min)
   - List all vets
   - View vet profile
   - Show appointments statistics

5. **API Integration** (1 min)
   - Open Postman
   - Test cross-system API calls
   - Show integration between systems

---

## 🌐 Deployment URLs

### After deploying to Render.com, update these:

```env
ADOPTION_SYSTEM_URL=https://pet-adoption-system.onrender.com
SHELTER_SYSTEM_URL=https://pet-shelter-system.onrender.com
VETERINARY_SYSTEM_URL=https://pet-veterinary-system.onrender.com
```

---

## 📚 Full Documentation

- 📖 [Complete Deployment Guide](DEPLOYMENT_GUIDE.md)
- 🔌 [API Integration Guide](POSTMAN_API_GUIDE.md)
- 📋 [Project README](README.md)

---

## ✅ Success!

Your Pet Adoption System is now deployed! 🎉

**Total time:** 5-15 minutes (depending on method)

**Need help?** Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
