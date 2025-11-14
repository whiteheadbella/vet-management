# 🧪 Pet Adoption System - Testing & Installation Guide

## ⚡ Quick Installation (5 Minutes)

### Step 1: Install Python Requirements
```powershell
# Navigate to project directory
cd C:\Users\white\OneDrive\Desktop\Vet-Management

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Initialize System
```powershell
# Check if everything is ready
python system_check.py

# Initialize all databases with sample data
python init_databases.py
```

### Step 3: Start All Systems
```powershell
# Option 1: Use startup script (opens 3 terminals)
python start_all.py

# Option 2: Manual start (open 3 PowerShell windows)
# Terminal 1:
python adoption_system/app.py

# Terminal 2:
python shelter_system/app.py

# Terminal 3:
python veterinary_system/app.py
```

### Step 4: Access the System
Open your browser and go to:
- **Main System**: http://localhost:5000
- **Shelter System**: http://localhost:5001
- **Veterinary System**: http://localhost:5002

---

## 🧪 Complete Testing Guide

### Test Scenario 1: User Registration & Login

#### Test as Adopter
1. Go to http://localhost:5000
2. Click "Register"
3. Fill form:
   - Name: Test Adopter
   - Email: test.adopter@test.com
   - Password: test123
   - Role: Pet Adopter
4. Click "Create Account"
5. Login with credentials

**Expected Result**: ✅ Redirected to home page, user menu shows name

---

### Test Scenario 2: Browse and View Pets

#### Browse Available Pets
1. Login as adopter
2. Click "Browse Pets" in navigation
3. Try filters:
   - Select "Dogs" only
   - Select "Cats" only
   - Enter breed name
   - Filter by age

**Expected Result**: ✅ Pet list updates based on filters

#### View Pet Details
1. Click on any pet card
2. View complete pet information
3. Check health indicators (vaccinated, spayed/neutered)

**Expected Result**: ✅ Detailed pet page with all information

---

### Test Scenario 3: Submit Adoption Application

#### Apply for Pet Adoption
1. Login as adopter (test.adopter@test.com)
2. Browse pets
3. Select a pet
4. Click "Apply for Adoption"
5. Fill application form:
   - Why do you want to adopt: "Looking for a family companion"
   - Previous pet experience: "Had a dog for 10 years"
   - Living situation: "House"
   - Has yard: Yes
   - Other pets: "None"
6. Submit application

**Expected Result**: ✅ Application submitted, confirmation email sent

#### Check Application Status
1. Go to Dashboard
2. View "My Applications"
3. Check application status (should be "pending")

**Expected Result**: ✅ Application listed with pending status

---

### Test Scenario 4: Shelter Staff - Manage Pets

#### Login as Shelter Staff
1. Logout from adopter account
2. Login with:
   - Email: shelter@example.com
   - Password: password123

#### Add New Pet
1. Go to http://localhost:5001/manage/pets
2. Click "Add Pet"
3. Fill form:
   - Name: Buddy
   - Species: Dog
   - Breed: Labrador Retriever
   - Age: 2
   - Gender: Male
   - Description: "Friendly and energetic"
   - Vaccinated: Yes
   - Spayed/Neutered: Yes
4. Submit

**Expected Result**: ✅ Pet added to shelter inventory

#### Review Applications
1. Go to http://localhost:5000/adoption/applications
2. View pending applications
3. Click on an application
4. Choose "Approve" or "Reject"
5. Add notes
6. Submit decision

**Expected Result**: ✅ Application status updated, notification sent to adopter

---

### Test Scenario 5: View Adopted Pets

#### As Adopter with Approved Application
1. Login as adopter
2. Go to Dashboard
3. Click "My Pets"
4. View adopted pet details
5. Check health records (if available)

**Expected Result**: ✅ Adopted pets displayed with health information

---

### Test Scenario 6: Veterinarian - Health Records

#### Login as Veterinarian
1. Login with:
   - Email: vet@example.com
   - Password: password123

#### Add Health Record
1. Go to http://localhost:5002
2. Click "Health Records"
3. Select a pet or create new record
4. Enter:
   - Weight: 25.5 kg
   - Temperature: 38.5°C
   - Vaccinations: Rabies, Distemper
   - Notes: "Annual checkup - healthy"
5. Save record

**Expected Result**: ✅ Health record created/updated

#### Schedule Appointment
1. Go to "Appointments"
2. Click "Schedule New"
3. Fill form:
   - Select pet
   - Select veterinarian
   - Choose date/time
   - Reason: "Annual checkup"
4. Submit

**Expected Result**: ✅ Appointment scheduled, calendar event created

---

### Test Scenario 7: API Testing

#### Test Shelter API
```powershell
# Get all pets
Invoke-WebRequest -Uri "http://localhost:5001/api/pets/" -Method GET

# Get specific pet
Invoke-WebRequest -Uri "http://localhost:5001/api/pets/1" -Method GET

# Get shelter statistics
Invoke-WebRequest -Uri "http://localhost:5001/api/stats" -Method GET
```

#### Test Veterinary API
```powershell
# Get health records
Invoke-WebRequest -Uri "http://localhost:5002/api/health/1" -Method GET

# Get all records
Invoke-WebRequest -Uri "http://localhost:5002/api/records" -Method GET
```

**Expected Result**: ✅ JSON responses with data

---

### Test Scenario 8: External API Integration

#### Test Dog API
1. Browse dogs in adoption system
2. View a dog's detailed page
3. Check if dog breed information loads
4. Verify dog breed images display

**Expected Result**: ✅ Dog breed info and images from Dog CEO API

#### Test Cat API
1. Browse cats in adoption system
2. View a cat's detailed page
3. Check if cat breed information loads

**Expected Result**: ✅ Cat breed details from The Cat API

---

## ✅ Verification Checklist

Use this checklist to verify all features:

### User Management
- [ ] User can register
- [ ] User can login
- [ ] User can logout
- [ ] User can view profile
- [ ] User can edit profile
- [ ] User can change password

### Pet Management (Shelter)
- [ ] Can add new pet
- [ ] Can edit pet details
- [ ] Can delete pet
- [ ] Can upload pet images
- [ ] Can update pet status
- [ ] Can view pet logs

### Adoption Process
- [ ] Can browse available pets
- [ ] Can filter pets by criteria
- [ ] Can view pet details
- [ ] Can submit adoption application
- [ ] Can view application status
- [ ] Shelter can review applications
- [ ] Shelter can approve/reject applications
- [ ] Adopted pets marked correctly

### Health Records (Veterinary)
- [ ] Can create health record
- [ ] Can update health record
- [ ] Can add vaccinations
- [ ] Can view pet health history
- [ ] Records accessible to adopters

### Appointments
- [ ] Can schedule appointment
- [ ] Can view appointments
- [ ] Can update appointment status
- [ ] Can cancel appointment
- [ ] Calendar integration works

### Email Notifications
- [ ] Welcome email on registration
- [ ] Application received confirmation
- [ ] Application status update
- [ ] Appointment reminders (if configured)

### API Integration
- [ ] Shelter API returns pet data
- [ ] Veterinary API returns health data
- [ ] Systems communicate correctly
- [ ] Dog API integration works
- [ ] Cat API integration works

---

## 🐛 Known Issues & Workarounds

### Issue: Email not sending
**Cause**: SMTP not configured
**Workaround**: 
1. Check `.env` file for correct SMTP settings
2. For Gmail, use App Password (not regular password)
3. System works without email, just no notifications

### Issue: Google Calendar not working
**Cause**: Credentials not configured
**Workaround**:
1. System works without Google Calendar
2. Appointments still created in database
3. To enable: Get credentials.json from Google Cloud Console

### Issue: Cat API showing "No data"
**Cause**: API key not configured
**Workaround**:
1. Get free API key from https://thecatapi.com/
2. Add to `.env` file: `CAT_API_KEY=your-key`
3. Dog API works without key

---

## 📊 Performance Testing

### Load Test Setup
```powershell
# Install load testing tool
pip install locust

# Create locustfile.py
# (See example in docs/)

# Run load test
locust -f locustfile.py
```

### Expected Performance
- **Response Time**: < 200ms for page loads
- **API Response**: < 100ms for queries
- **Concurrent Users**: 50+ without issues
- **Database Queries**: < 50ms average

---

## 🔍 Debug Mode

Enable detailed error messages:

```powershell
# In .env file
FLASK_ENV=development
FLASK_DEBUG=True
```

This will show:
- Detailed error traces
- SQL queries
- Template rendering info
- Request/response data

---

## 📝 Test Data Reset

To reset all test data:

```powershell
# Stop all systems first (Ctrl+C in each terminal)

# Delete databases
Remove-Item adoption_system/adoption_system.db
Remove-Item shelter_system/shelter_system.db
Remove-Item veterinary_system/veterinary_system.db

# Reinitialize
python init_databases.py

# Restart systems
python start_all.py
```

---

## 🎓 Learning Exercises

Try these to learn more about the system:

### Exercise 1: Add a New Field
1. Add "Color" field to adoption application
2. Update form template
3. Update model
4. Update database

### Exercise 2: Create Custom Report
1. Create "Monthly Adoptions" report
2. Query database for adoption statistics
3. Display in dashboard

### Exercise 3: Add Email Template
1. Create HTML email template
2. Add to email service
3. Send formatted emails

### Exercise 4: Extend API
1. Add new endpoint: /api/featured-pets
2. Return 3 random featured pets
3. Display on homepage

---

## 📞 Getting Help

If tests fail:

1. **Check Terminal Output**: Error messages appear here
2. **Run System Check**: `python system_check.py`
3. **Verify Database**: Ensure .db files exist
4. **Check Logs**: Look for error traces
5. **Review Documentation**: Check QUICKSTART.md

---

## ✨ Success Criteria

Your system is working correctly if:

✅ All three systems start without errors
✅ You can register and login
✅ Pets are visible and browseable
✅ Applications can be submitted
✅ Shelter can approve applications
✅ Health records are accessible
✅ No database errors in terminal
✅ Pages load within 2 seconds

---

**Happy Testing! 🎉**

Remember: This is a learning project. Don't worry if everything isn't perfect - focus on understanding how the systems work together!
