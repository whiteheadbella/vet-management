# 🚀 Team Member Setup Guide - Step by Step

## Complete Guide for Team Members to Clone and Run the Project

---

## ✅ Prerequisites

Before starting, make sure you have:
- [ ] Windows 10/11 (PowerShell 5.1 or higher)
- [ ] Python 3.11 or higher
- [ ] Git installed
- [ ] Internet connection
- [ ] GitHub account (optional, for private repos)

### Check Your Installations:

```powershell
# Check Python version (should be 3.11+)
python --version

# Check Git version
git --version

# Check PowerShell version (should be 5.1+)
$PSVersionTable.PSVersion
```

If anything is missing, install it first:
- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/download/win

---

## 📥 STEP 1: Clone the Repository

### 1.1 Open PowerShell

- Press `Win + X`
- Select "Windows PowerShell" or "Terminal"

### 1.2 Navigate to Your Desired Location

```powershell
# Navigate to Desktop (or wherever you want the project)
cd $HOME\Desktop

# Or create a dedicated projects folder
mkdir Projects
cd Projects
```

### 1.3 Clone the Repository

```powershell
# Clone the project
git clone https://github.com/whiteheadbella/vet-management.git

# Navigate into the project folder
cd vet-management
```

**Expected Output:**
```
Cloning into 'vet-management'...
remote: Enumerating objects: 125, done.
remote: Counting objects: 100% (125/125), done.
remote: Compressing objects: 100% (116/116), done.
remote: Total 125 (delta 20), reused 125 (delta 20)
Receiving objects: 100% (125/125), 150.66 KiB | 3.35 MiB/s, done.
Resolving deltas: 100% (20/20), done.
```

✅ **Checkpoint:** You should now see a `vet-management` folder with all project files.

---

## 📦 STEP 2: Install Python Dependencies

### 2.1 Verify You're in the Project Directory

```powershell
# Check current location (should show vet-management)
pwd

# List files (should see adoption_system, shelter_system, etc.)
ls
```

### 2.2 Install Required Packages

```powershell
# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0-py3-none-any.whl
Collecting Flask-SQLAlchemy==3.1.1
  Downloading Flask_SQLAlchemy-3.1.1-py3-none-any.whl
...
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 ...
```

**⏱️ This takes 2-3 minutes**

### 2.3 Verify Installation

```powershell
# Check if Flask is installed
pip show Flask

# List all installed packages
pip list
```

✅ **Checkpoint:** You should see Flask, SQLAlchemy, and other packages listed.

---

## 🗄️ STEP 3: Initialize Databases

### 3.1 Create Database Tables

```powershell
# Initialize all three databases
python init_databases.py
```

**Expected Output:**
```
Initializing databases for all three systems...
Creating Adoption System database...
✓ Adoption System database initialized!
Creating Shelter System database...
✓ Shelter System database initialized!
Creating Veterinary System database...
✓ Veterinary System database initialized!
All databases initialized successfully!
```

### 3.2 Populate with Sample Data

```powershell
# Add 20 sample pets with images
python populate_pets.py
```

**Expected Output:**
```
Populating pets database with sample data...
Adding 10 dogs...
  ✓ Max (Golden Retriever) added
  ✓ Buddy (Labrador Retriever) added
  ...
Adding 10 cats...
  ✓ Luna (Persian) added
  ✓ Whiskers (Siamese) added
  ...
Successfully added 20 pets!
```

**⏱️ This takes 1-2 minutes (downloading images from APIs)**

### 3.3 Add Health Records and Appointments

```powershell
# Populate veterinary data
python populate_vet_records.py
```

**Expected Output:**
```
Adding veterinarians...
  ✓ Dr. Sarah Smith added
  ✓ Dr. Michael Johnson added
  ✓ Dr. Emily Brown added
Adding health records...
  ✓ 20 health records added
Adding appointments...
  ✓ 5 appointments scheduled
Veterinary data populated successfully!
```

✅ **Checkpoint:** You should now have three .db files in your project folder:
- `adoption_system.db`
- `shelter_system.db`
- `veterinary_system.db`

---

## 🚀 STEP 4: Start All Servers

### 4.1 Run the Startup Script

```powershell
# Start all three systems at once
.\start_all_servers.ps1
```

**What Happens:**
- 3 new PowerShell windows will open
- Each window runs one system:
  - Window 1: Adoption System (Port 5000) - Green text
  - Window 2: Shelter System (Port 5001) - Green text
  - Window 3: Veterinary System (Port 5002) - Green text
- Your default browser will open to http://localhost:5000

**Expected Output in Each Window:**
```
Adoption System - Port 5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.x:5000
Press CTRL+C to quit
```

**⏱️ Wait 10-15 seconds for all servers to start**

✅ **Checkpoint:** All 3 PowerShell windows should show "Running on http://127.0.0.1:xxxx"

---

## 🌐 STEP 5: Access the Systems

### 5.1 Open in Your Browser

Click these links or type in your browser:

**Adoption System (Public Site):**
```
http://localhost:5000
```
- Browse pets
- View pet details
- Apply for adoption

**Shelter Management System (Admin):**
```
http://localhost:5001
```
- Add new pets
- Update pet status
- Manage inventory
- View activity logs

**Veterinary System (Medical Records):**
```
http://localhost:5002
```
- View health records
- Schedule appointments
- Manage veterinarians

### 5.2 Test the Integration

1. **Browse Pets:**
   - Go to http://localhost:5000
   - Click "Browse Pets"
   - You should see 20 pets (10 dogs, 10 cats)

2. **View Pet Details:**
   - Click "View Details" on any pet
   - You should see:
     - Pet information
     - Multiple images (carousel)
     - Health records (from Vet System API)

3. **Add a New Pet:**
   - Go to http://localhost:5001
   - Click "Add Pet"
   - Fill in the form
   - Submit
   - Check if it appears in the Adoption System

✅ **Checkpoint:** All systems should be accessible and showing data.

---

## 🛑 STEP 6: Stopping the Servers

### Option 1: Close the Windows
- Simply close the 3 PowerShell windows
- Servers will stop automatically

### Option 2: Use Stop Command
```powershell
# In a new PowerShell window, run:
Get-Process python | Stop-Process -Force
```

---

## 🔧 STEP 7: Restart After Stopping

Next time you want to run the project:

```powershell
# 1. Navigate to project folder
cd $HOME\Desktop\vet-management

# 2. Start servers
.\start_all_servers.ps1

# That's it! Databases are already set up.
```

---

## 📱 STEP 8: Share with Others (Optional)

If you want to share your local project with others on the same network:

### 8.1 Find Your Local IP

```powershell
# Get your computer's IP address
ipconfig | Select-String "IPv4"
```

**Example Output:** `IPv4 Address: 192.168.1.112`

### 8.2 Share These URLs

Give these to teammates on the same WiFi/network:
```
Adoption:  http://192.168.1.112:5000
Shelter:   http://192.168.1.112:5001
Vet:       http://192.168.1.112:5002
```

---

## ⚠️ TROUBLESHOOTING

### Problem 1: "Python is not recognized"
**Solution:**
```powershell
# Add Python to PATH
# Reinstall Python and check "Add Python to PATH" during installation
```

### Problem 2: "Port already in use"
**Solution:**
```powershell
# Kill processes on ports 5000, 5001, 5002
Get-Process python | Stop-Process -Force
# Wait 5 seconds, then restart
.\start_all_servers.ps1
```

### Problem 3: "Module not found" errors
**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem 4: "No pets showing" in browser
**Solution:**
```powershell
# Re-populate database
python populate_pets.py
```

### Problem 5: "Database is locked"
**Solution:**
```powershell
# Stop all servers
Get-Process python | Stop-Process -Force
# Wait 5 seconds
# Delete .db files and reinitialize
Remove-Item *.db
python init_databases.py
python populate_pets.py
python populate_vet_records.py
```

### Problem 6: PowerShell script won't run
**Solution:**
```powershell
# Allow script execution (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again
.\start_all_servers.ps1
```

---

## 📚 USEFUL COMMANDS

### Check System Status
```powershell
# Check if servers are running
Get-Process python

# Check which ports are in use
netstat -ano | findstr ":5000 :5001 :5002"
```

### Update from GitHub (if main repo changes)
```powershell
# Get latest changes
git pull origin main

# Reinstall dependencies (if requirements.txt changed)
pip install -r requirements.txt
```

### View Logs
```powershell
# Each PowerShell window shows live logs
# Look for errors in red
```

---

## 🎯 QUICK REFERENCE

### Project URLs:
| System | URL | Purpose |
|--------|-----|---------|
| Adoption | http://localhost:5000 | Public pet browsing |
| Shelter | http://localhost:5001 | Admin management |
| Veterinary | http://localhost:5002 | Medical records |

### Important Files:
| File | Purpose |
|------|---------|
| `start_all_servers.ps1` | Start all 3 systems |
| `requirements.txt` | Python dependencies |
| `init_databases.py` | Create database tables |
| `populate_pets.py` | Add sample pets |
| `config.py` | Configuration settings |

### Key Folders:
| Folder | Contents |
|--------|----------|
| `adoption_system/` | Public adoption platform |
| `shelter_system/` | Shelter management |
| `veterinary_system/` | Vet records system |
| `*.db` | Database files |

---

## 🎓 WHAT YOU SHOULD SEE

### Adoption System Homepage:
- Hero section with "Find Your Perfect Pet"
- 3 feature cards (Browse, Apply, Care)
- "Browse Pets" button

### Browse Pets Page:
- Filter by species, breed, age, gender
- Grid of pet cards with images
- "View Details" buttons

### Shelter Management Dashboard:
- Statistics (Total pets, Available, Adopted, Pending)
- Feature cards (Add Pet, Update Status, Upload Images, API Sync)
- Recent additions list
- Activity log

### Add Pet Form:
- Basic information (name, species, breed, age, gender)
- Medical information (textarea, checkboxes)
- Behavioral traits
- Image upload
- Staff name field

### Veterinary System:
- Veterinarian list
- Health records table
- Appointment scheduler

---

## ✅ VERIFICATION CHECKLIST

- [ ] Project cloned successfully
- [ ] All dependencies installed
- [ ] Databases initialized
- [ ] Sample data populated
- [ ] All 3 servers running
- [ ] Can access http://localhost:5000
- [ ] Can access http://localhost:5001
- [ ] Can access http://localhost:5002
- [ ] Can browse pets
- [ ] Can view pet details
- [ ] Can see health records on pet detail page
- [ ] Can add a new pet from shelter system
- [ ] New pet appears in adoption system

---

## 📞 NEED HELP?

### Resources:
- **Project Documentation:** Check all .md files in the project
- **GitHub Issues:** https://github.com/whiteheadbella/vet-management/issues
- **README.md:** General project overview
- **TROUBLESHOOTING.md:** Common issues and fixes

### Contact:
- **Developer:** Bella Whitehead
- **Repository:** https://github.com/whiteheadbella/vet-management

---

## 🎉 SUCCESS!

If you've completed all steps, you now have a fully functional Pet Adoption Management System running locally!

**Next Steps:**
1. Explore all three systems
2. Try adding a new pet
3. Schedule a vet appointment
4. Test the API integration
5. Read the PROJECT_REPORT.md for technical details

**Happy coding!** 🐾
