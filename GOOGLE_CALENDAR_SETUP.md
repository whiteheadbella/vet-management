# Google Calendar Integration Setup Guide

## 🗓️ Overview

The Veterinary Management System has built-in Google Calendar integration that automatically:
- ✅ Creates calendar events when appointments are scheduled
- ✅ Updates events when appointments are modified
- ✅ Deletes events when appointments are cancelled
- ✅ Stores `google_calendar_event_id` in the database
- ✅ Sends email reminders to pet owners

## 📋 Prerequisites

1. **Google Account** with Google Calendar access
2. **Google Cloud Project** with Calendar API enabled
3. **OAuth 2.0 Credentials** downloaded

## 🚀 Quick Setup (5 Steps)

### Step 1: Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Calendar API**:
   - Navigate to **APIs & Services** > **Library**
   - Search for "Google Calendar API"
   - Click **Enable**

### Step 2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Choose **Desktop app** as application type
4. Name it: `Vet Management System`
5. Click **Create**
6. Download the credentials JSON file

### Step 3: Configure Credentials

1. Rename the downloaded file to `credentials.json`
2. Place it in the project root directory:
   ```
   Vet-Management/
   ├── credentials.json  ← Place here
   ├── config.py
   └── ...
   ```

### Step 4: Install Google API Library

```powershell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 5: Update Configuration

Edit `config.py` to ensure these settings exist:

```python
GOOGLE_CALENDAR_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
GOOGLE_CALENDAR_TOKEN_FILE = os.path.join(BASE_DIR, 'token.pickle')
```

## ✅ First Time Setup

When you schedule your first appointment:

1. The system will open your browser
2. Login with your Google account
3. Grant calendar permissions
4. A `token.pickle` file will be created (saved for future use)
5. The appointment will appear in your Google Calendar

## 🎯 How It Works

### When Creating an Appointment:

```python
# Automatically called when scheduling appointment
appointment = Appointment(
    pet_name="Max",
    owner_email="owner@example.com",
    date=datetime(2025, 11, 15, 10, 0),
    duration=30,
    reason="Annual checkup"
)

# Google Calendar event is created automatically
# google_calendar_event_id is stored in database
```

### Database Schema:

```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER,
    pet_name VARCHAR(100),
    owner_name VARCHAR(100),
    owner_email VARCHAR(120),
    vet_id INTEGER,
    date DATETIME,
    duration INTEGER DEFAULT 30,
    reason VARCHAR(200),
    status VARCHAR(20) DEFAULT 'scheduled',
    google_calendar_event_id VARCHAR(200),  ← Stores Google event ID
    created_at DATETIME,
    updated_at DATETIME
);
```

## 📊 Calendar Event Details

Each appointment creates a calendar event with:

- **Title**: `Vet Appointment - [Pet Name]`
- **Description**: Reason for visit + owner contact info
- **Duration**: Configurable (default 30 minutes)
- **Reminders**: 
  - Email reminder 24 hours before
  - Popup reminder 1 hour before
- **Attendees**: Pet owner's email (receives invite)

## 🔧 Testing the Integration

### 1. Check if Google Calendar is Available:

```powershell
# Run this in PowerShell
python -c "from veterinary_system.utils.google_calendar import GOOGLE_AVAILABLE; print('Google Calendar:', 'Available' if GOOGLE_AVAILABLE else 'Not Available')"
```

### 2. Schedule a Test Appointment:

1. Go to **http://localhost:5002**
2. Login as veterinarian:
   - Email: `vet@example.com`
   - Password: `password123`
3. Navigate to **Appointments** > **Schedule New**
4. Fill in appointment details
5. Click **Schedule**
6. Check your Google Calendar!

### 3. Verify Database Storage:

```sql
-- Check if google_calendar_event_id is stored
SELECT id, pet_name, date, status, google_calendar_event_id 
FROM appointments 
WHERE google_calendar_event_id IS NOT NULL;
```

## 🎨 Calendar Event Features

### Automatic Updates:
- ✅ Reschedule appointment → Calendar event updates automatically
- ✅ Cancel appointment → Calendar event deleted automatically
- ✅ Complete appointment → Status updated (event remains)

### Email Notifications:
- Owner receives Google Calendar invite
- Automatic reminders sent by Google
- Can accept/decline/add to their own calendar

## 🔒 Security & Privacy

- **OAuth 2.0** authentication (industry standard)
- **Token stored locally** in `token.pickle`
- **Credentials never exposed** in code
- **User consent required** first time only
- **Revoke access anytime** in Google Account settings

## 🐛 Troubleshooting

### Issue: "Google Calendar API not available"
**Solution**: Install required packages
```powershell
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Issue: "Credentials file not found"
**Solution**: 
1. Download credentials from Google Cloud Console
2. Rename to `credentials.json`
3. Place in project root directory

### Issue: "Token expired"
**Solution**: Delete `token.pickle` and re-authenticate
```powershell
Remove-Item token.pickle
```

### Issue: Calendar event not created
**Solution**: Check console logs for errors
```python
# Events are created in: veterinary_system/routes/appointments.py
# Line 55-70 (create_calendar_event function)
```

## 📱 Mobile Access

Calendar events sync to:
- ✅ Google Calendar mobile app
- ✅ Gmail calendar view
- ✅ Other devices linked to Google account

## 🎓 For Presentation Demo

### Show the Integration:

1. **Schedule Appointment**:
   - Show creating appointment in Vet System (Port 5002)
   - Open Google Calendar
   - Show event appears automatically

2. **Update Appointment**:
   - Reschedule appointment in system
   - Show calendar event updates in real-time

3. **Cancel Appointment**:
   - Cancel in system
   - Show event removed from calendar

4. **Database Proof**:
   - Show `google_calendar_event_id` in database
   - Explain the link between systems

## 📖 API Reference

### Available Functions:

```python
# Create calendar event
from veterinary_system.utils.google_calendar import create_calendar_event

event_id = create_calendar_event(
    title="Vet Appointment - Max",
    description="Annual checkup",
    start_time=datetime(2025, 11, 15, 10, 0),
    duration=30,
    attendees=["owner@example.com"]
)

# Update calendar event
from veterinary_system.utils.google_calendar import update_calendar_event

update_calendar_event(
    event_id="abc123",
    title="Updated Title",
    start_time=datetime(2025, 11, 16, 14, 0)
)

# Delete calendar event
from veterinary_system.utils.google_calendar import delete_calendar_event

delete_calendar_event("abc123")
```

## ✨ Benefits

1. **Automatic Sync**: No manual calendar entry needed
2. **Owner Notifications**: Pet owners receive reminders
3. **Cross-Platform**: Works on web, mobile, desktop
4. **Conflict Detection**: Google Calendar prevents double-booking
5. **Professional**: Automated reminders improve attendance

## 🔗 Useful Links

- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)

---

**Need Help?** The integration code is in:
- `veterinary_system/utils/google_calendar.py` - Calendar functions
- `veterinary_system/routes/appointments.py` - Appointment handling
- `veterinary_system/models.py` - Database schema (line 185)

**Status**: ✅ **Fully Implemented** - Just needs credentials to activate!
