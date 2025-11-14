# 🚀 How to Run Each Server - Step by Step

## ⚡ Quick Start (3 Steps)

### Step 1: Initialize Everything (One Time)

Open PowerShell in your project folder:
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
```

Run these commands **one time only**:
```powershell
# Initialize databases
python init_databases.py

# Populate with 20 pets
python populate_pets.py

# Populate with health records
python populate_vet_records.py
```

---

### Step 2: Start the Servers

**You need 3 separate PowerShell windows:**

#### PowerShell Window 1 - Adoption System (Port 5000)
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
python adoption_system/app.py
```

#### PowerShell Window 2 - Shelter System (Port 5001)
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
python shelter_system/app.py
```

#### PowerShell Window 3 - Veterinary System (Port 5002)
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
python veterinary_system/app.py
```

---

### Step 3: Access the Systems

Open your browser:
- **Adoption System (Browse Pets)**: http://localhost:5000
- **Shelter System**: http://localhost:5001
- **Veterinary System**: http://localhost:5002

---

## 🎯 Alternative: Run All at Once

Use this script to start all 3 servers automatically:

```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Start Adoption System (Port 5000)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python adoption_system/app.py"

# Wait 3 seconds
Start-Sleep -Seconds 3

# Start Shelter System (Port 5001)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python shelter_system/app.py"

# Wait 3 seconds
Start-Sleep -Seconds 3

# Start Veterinary System (Port 5002)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python veterinary_system/app.py"
```

This will open 3 PowerShell windows automatically!

---

## 🔍 Verify Everything is Working

After starting the servers, run this check:

```powershell
# Check if servers are responding
curl http://localhost:5000
curl http://localhost:5001
curl http://localhost:5002

# Check if pets API works
curl http://localhost:5001/api/pets/
```

---

## 🛑 To Stop Servers

### Option 1: Close PowerShell Windows
Just close the 3 PowerShell windows where servers are running

### Option 2: Stop All Python Processes
```powershell
Get-Process python | Stop-Process -Force
```

### Option 3: Press CTRL+C in each window
In each PowerShell window running a server, press `CTRL+C`

---

## ❓ Troubleshooting

### "No pets found" or empty pet list

**Problem:** Database not populated
**Solution:**
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
python populate_pets.py
python populate_vet_records.py
```

---

### "Port already in use" error

**Problem:** Server already running on that port
**Solution:**
```powershell
# Find and kill process on port 5000
$process = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($process) { Stop-Process -Id $process -Force }

# Or kill all Python processes
Get-Process python | Stop-Process -Force
```

---

### "Module not found" error

**Problem:** Missing dependencies
**Solution:**
```powershell
pip install -r requirements.txt
```

---

### Servers start but can't access in browser

**Problem:** Servers not binding to correct host/port
**Solution:** Check the terminal output for actual URLs, should show:
```
* Running on http://127.0.0.1:5000
```

---

## 📋 Complete Command Reference

### One-Time Setup:
```powershell
# Navigate to project
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Install dependencies
pip install -r requirements.txt

# Initialize databases
python init_databases.py

# Populate data
python populate_pets.py
python populate_vet_records.py
```

### Every Time You Want to Run:
```powershell
# Method 1: Manual (3 separate windows)
# Window 1:
python adoption_system/app.py

# Window 2:
python shelter_system/app.py

# Window 3:
python veterinary_system/app.py

# Method 2: Automatic (runs all 3)
.\deploy_local.ps1
```

### To Stop:
```powershell
# Stop all Python processes
Get-Process python | Stop-Process -Force
```

### To Check Status:
```powershell
# Check running Python processes
Get-Process python

# Check ports in use
Get-NetTCPConnection -LocalPort 5000,5001,5002 | Select-Object LocalPort, State, OwningProcess

# Test if servers respond
curl http://localhost:5000
curl http://localhost:5001
curl http://localhost:5002
```

---

## 🎬 Quick Demo Setup

**Before your presentation, run these commands:**

```powershell
# 1. Navigate to project
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# 2. Make sure data exists (only if not done before)
python populate_pets.py
python populate_vet_records.py

# 3. Start all servers
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python adoption_system/app.py"
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python shelter_system/app.py"
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python veterinary_system/app.py"

# 4. Wait 10 seconds for all to start
Start-Sleep -Seconds 10

# 5. Open browser
Start-Process "http://localhost:5000"
```

---

## ✅ Success Checklist

After running servers, you should have:
- [ ] 3 PowerShell windows open (one for each server)
- [ ] Each window showing "Running on http://127.0.0.1:XXXX"
- [ ] No error messages in the windows
- [ ] Can access http://localhost:5000 in browser
- [ ] Can see 20 pets when browsing
- [ ] Can view health records at http://localhost:5002

---

**Need more help?** See [README.md](README.md) or [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
