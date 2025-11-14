# 🔧 Troubleshooting Guide - Pet Adoption System

## 🚨 Common Problems & Solutions

### 1. Installation Issues

#### Problem: "python: command not found"
**Solution:**
```powershell
# Verify Python installation
python --version
# or
python3 --version

# If not installed, download from python.org
# Make sure to check "Add Python to PATH" during installation
```

#### Problem: "pip: command not found"
**Solution:**
```powershell
# Pip should come with Python. If missing:
python -m ensurepip --upgrade

# Or reinstall Python with pip included
```

#### Problem: "Cannot activate virtual environment"
**Solution:**
```powershell
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
.\venv\Scripts\Activate.ps1
```

#### Problem: "Module not found" errors
**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall all dependencies
pip install -r requirements.txt

# If still failing, try:
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

---

### 2. Database Issues

#### Problem: "No such table" error
**Solution:**
```powershell
# Database not initialized
python init_databases.py

# If error persists, delete and recreate:
Remove-Item *_system/*.db
python init_databases.py
```

#### Problem: "Database is locked"
**Solution:**
```powershell
# Stop all running systems (Ctrl+C)
# Wait 5 seconds
# Restart systems

# If still locked:
# Close any SQLite browser tools
# Delete .db files and reinitialize
```

#### Problem: "Integrity error" when adding data
**Solution:**
```powershell
# Usually means duplicate data
# Check if record already exists
# Or delete and recreate database:
python init_databases.py
```

---

### 3. Port Issues

#### Problem: "Address already in use" - Port 5000
**Solution:**
```powershell
# Find what's using the port:
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual number):
taskkill /PID <PID> /F

# Or use different port in each app.py:
# Change: app.run(debug=True, port=5000)
# To:     app.run(debug=True, port=5003)
```

#### Problem: "Connection refused" between systems
**Solution:**
```powershell
# Make sure all three systems are running:
# Check http://localhost:5000 (Adoption)
# Check http://localhost:5001 (Shelter)
# Check http://localhost:5002 (Veterinary)

# Verify URLs in .env file:
ADOPTION_SYSTEM_URL=http://localhost:5000
SHELTER_SYSTEM_URL=http://localhost:5001
VETERINARY_SYSTEM_URL=http://localhost:5002
```

---

### 4. Template Issues

#### Problem: "Template not found" error
**Solution:**
```powershell
# Check template exists:
# adoption_system/templates/[folder]/[file].html

# Verify template name in route:
# return render_template('folder/file.html')

# Check spelling and capitalization
```

#### Problem: "TemplateNotFound: base.html"
**Solution:**
```powershell
# Create missing base template
# Copy from adoption_system/templates/base.html
# to other systems if needed

# Or check template inheritance:
# {% extends "base.html" %}
```

---

### 5. Import Errors

#### Problem: "ImportError: cannot import name 'db'"
**Solution:**
```powershell
# This is a circular import issue
# Make sure models.py has:
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# And app.py has:
from models import db
db.init_app(app)
```

#### Problem: "No module named 'routes'"
**Solution:**
```powershell
# Check directory structure:
# system_name/
#   ├── routes/
#   │   ├── __init__.py  # This file is needed!
#   │   └── auth.py

# Create __init__.py if missing:
New-Item routes/__init__.py -ItemType File
```

---

### 6. Login/Authentication Issues

#### Problem: "Invalid email or password"
**Solution:**
```powershell
# Use default credentials:
# Adopter:  adopter@example.com / password123
# Shelter:  shelter@example.com / password123
# Vet:      vet@example.com / password123

# If still failing, reinitialize database:
python init_databases.py
```

#### Problem: "Login required" redirect loop
**Solution:**
```python
# In app.py, check:
login_manager.login_view = 'auth.login'  # Should match your blueprint

# Or disable login requirement temporarily:
# Comment out @login_required decorators
```

#### Problem: Session not persisting
**Solution:**
```powershell
# Check SECRET_KEY in .env
SECRET_KEY=your-secret-key-here

# Must be set and not empty
```

---

### 7. API Integration Issues

#### Problem: "Connection timeout" to external APIs
**Solution:**
```powershell
# Check internet connection
# APIs might be down - try again later

# Test direct access:
Invoke-WebRequest -Uri "https://dog.ceo/api/breeds/list/all"
Invoke-WebRequest -Uri "https://api.thecatapi.com/v1/breeds"

# Add timeout handling in code
```

#### Problem: Cat API returns 401 Unauthorized
**Solution:**
```powershell
# Get free API key from https://thecatapi.com/
# Add to .env:
CAT_API_KEY=your-api-key-here

# Restart the system
```

#### Problem: "No pets found" when browsing
**Solution:**
```powershell
# Shelter system not running
# Start it: python shelter_system/app.py

# Or add sample pets:
python init_databases.py
```

---

### 8. Email Issues

#### Problem: "Connection refused" - SMTP
**Solution:**
```powershell
# Email is optional - system works without it

# To enable Gmail:
# 1. Enable 2-Factor Authentication
# 2. Generate App Password
# 3. Update .env:
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

#### Problem: "SMTPAuthenticationError"
**Solution:**
```powershell
# For Gmail:
# - Use App Password (not regular password)
# - Enable "Less secure app access" (if no 2FA)

# For other providers:
# Check MAIL_SERVER and MAIL_PORT settings
```

---

### 9. File Upload Issues

#### Problem: "413 Request Entity Too Large"
**Solution:**
```python
# In config.py, increase:
MAX_CONTENT_LENGTH = 16777216  # 16MB

# Or in .env:
MAX_CONTENT_LENGTH=16777216
```

#### Problem: "File type not allowed"
**Solution:**
```python
# In config.py, add extensions:
ALLOWED_EXTENSIONS = 'png,jpg,jpeg,gif,webp'

# Or check file has valid extension
```

#### Problem: Uploaded images not showing
**Solution:**
```powershell
# Check upload directory exists:
Test-Path adoption_system/static/uploads

# Create if missing:
New-Item -ItemType Directory -Path adoption_system/static/uploads

# Check file permissions
```

---

### 10. Performance Issues

#### Problem: "System is slow"
**Solution:**
```powershell
# Add database indexes:
# In models.py, add index=True to frequently queried fields

# Enable caching:
pip install Flask-Caching

# Optimize queries:
# Use .join() instead of multiple queries
# Add pagination to large lists
```

#### Problem: "High memory usage"
**Solution:**
```powershell
# Restart systems periodically
# Close unused database connections
# Limit query results with pagination
```

---

### 11. Google Calendar Issues

#### Problem: "Credentials file not found"
**Solution:**
```powershell
# Google Calendar is optional - system works without it

# To enable:
# 1. Go to Google Cloud Console
# 2. Create project & enable Calendar API
# 3. Download credentials.json
# 4. Place in veterinary_system/

# System will prompt for authorization on first use
```

---

## 🔍 Debugging Techniques

### Enable Debug Mode
```python
# In each app.py:
app.run(debug=True, port=5000)

# This shows detailed errors in browser
```

### Check Logs
```powershell
# Terminal output shows all errors
# Save to file:
python adoption_system/app.py > adoption.log 2>&1
```

### Test Database Directly
```powershell
# Install SQLite browser or use Python:
python
>>> from adoption_system.models import *
>>> from adoption_system.app import app
>>> with app.app_context():
...     users = User.query.all()
...     print(users)
```

### Test API Endpoints
```powershell
# Test Shelter API:
Invoke-WebRequest -Uri "http://localhost:5001/api/pets/" | ConvertFrom-Json

# Test Veterinary API:
Invoke-WebRequest -Uri "http://localhost:5002/api/health/1" | ConvertFrom-Json
```

---

## 🆘 Emergency Fixes

### Nuclear Option 1: Complete Reset
```powershell
# Stop all systems
# Delete everything and start over:
Remove-Item -Recurse venv/
Remove-Item *_system/*.db
Remove-Item -Recurse *_system/__pycache__/

# Reinstall:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_databases.py
```

### Nuclear Option 2: Fresh Clone
```powershell
# If using Git:
cd ..
git clone [repository] Vet-Management-Backup
cd Vet-Management-Backup
# Follow installation steps
```

---

## 📞 Getting More Help

### Before Asking for Help, Collect:
1. **Error Message**: Full text from terminal
2. **What You Did**: Steps to reproduce
3. **System Info**: `python --version`, OS version
4. **Which System**: Adoption/Shelter/Veterinary
5. **When It Happens**: Always/sometimes/specific action

### Check These First:
- [ ] All three systems are running
- [ ] Virtual environment is activated
- [ ] Databases are initialized
- [ ] .env file exists
- [ ] No typos in URLs/routes
- [ ] Internet connection (for external APIs)

### Diagnostic Command
```powershell
# Run full system check:
python system_check.py

# This checks:
# - Python version
# - Dependencies
# - Files & directories
# - Databases
# - Configuration
```

---

## 🎯 Quick Reference

### Restart Everything
```powershell
# Stop all (Ctrl+C in each terminal)
python start_all.py
```

### Check System Status
```powershell
# Test if systems are responding:
Invoke-WebRequest -Uri "http://localhost:5000"
Invoke-WebRequest -Uri "http://localhost:5001"
Invoke-WebRequest -Uri "http://localhost:5002"
```

### Reset Single System
```powershell
# Example for adoption system:
Remove-Item adoption_system/adoption_system.db
cd adoption_system
python -c "from app import app, db; app.app_context().push(); db.create_all()"
cd ..
```

---

## ✅ Prevention Tips

1. **Always activate venv** before running commands
2. **Don't edit code while system is running** (restart after changes)
3. **Keep backups** of working .db files
4. **Test in development** before production
5. **Read error messages** - they usually tell you what's wrong
6. **Use system_check.py** before starting work
7. **Document changes** you make to configuration

---

**Remember**: Most issues are simple typos or missing steps. Take a deep breath, read the error message carefully, and try the solutions above! 🚀
