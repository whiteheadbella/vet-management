# Pet Adoption System - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Installation Steps

1. **Navigate to the project directory**
```powershell
cd C:\Users\white\OneDrive\Desktop\Vet-Management
```

2. **Create a virtual environment** (recommended)
```powershell
python -m venv venv
```

3. **Activate the virtual environment**
```powershell
.\venv\Scripts\Activate.ps1
# If you get an error about execution policy, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. **Install dependencies**
```powershell
pip install -r requirements.txt
```

5. **Create environment file**
```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Edit .env file and update configurations (optional for local development)
notepad .env
```

6. **Initialize databases**
```powershell
python init_databases.py
```

This will:
- Create all database tables
- Add sample data (users, pets, vets)
- Create upload directories

### Running the Systems

You need to run all three systems in separate terminal windows:

**Terminal 1 - Adoption System (Main Hub)**
```powershell
cd adoption_system
python app.py
```
Access at: http://localhost:5000

**Terminal 2 - Shelter System**
```powershell
cd shelter_system
python app.py
```
Access at: http://localhost:5001

**Terminal 3 - Veterinary System**
```powershell
cd veterinary_system
python app.py
```
Access at: http://localhost:5002

## 👤 Default Login Credentials

### Adopter Account
- Email: `adopter@example.com`
- Password: `password123`
- Use this to browse and adopt pets

### Shelter Staff Account
- Email: `shelter@example.com`
- Password: `password123`
- Use this to manage pets and approve adoptions

### Veterinarian Account
- Email: `vet@example.com`
- Password: `password123`
- Use this to manage health records and appointments

## 📱 System Overview

### 1. Adoption System (Port 5000)
**Main user-facing platform**
- Browse available pets
- Submit adoption applications
- View adoption history
- Access pet health records
- Schedule vet appointments

**Key URLs:**
- Home: http://localhost:5000
- Browse Pets: http://localhost:5000/pets/browse
- Dashboard: http://localhost:5000/dashboard
- Login: http://localhost:5000/auth/login

### 2. Shelter Inventory System (Port 5001)
**Backend system for shelter management**
- Add/edit/delete pets
- Upload pet images
- Track pet status (available/adopted)
- View shelter logs

**Key URLs:**
- Dashboard: http://localhost:5001/dashboard
- Manage Pets: http://localhost:5001/manage/pets
- API Endpoint: http://localhost:5001/api/pets/

### 3. Veterinary Management System (Port 5002)
**Health records and appointments**
- Manage pet health records
- Track vaccinations
- Schedule appointments
- Google Calendar integration

**Key URLs:**
- Dashboard: http://localhost:5002/dashboard
- Appointments: http://localhost:5002/appointments/list
- Vets: http://localhost:5002/vets/

## 🔧 Configuration

### Email Notifications
To enable email notifications, update `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate an "App Password"
3. Use that password in the config

### Cat API
To use Cat API features:
1. Get free API key from https://thecatapi.com/
2. Add to `.env`: `CAT_API_KEY=your-key-here`

### Google Calendar API
For appointment scheduling:
1. Go to Google Cloud Console
2. Create a project
3. Enable Google Calendar API
4. Download credentials.json
5. Place in veterinary_system folder

## 🎯 Testing the System

### Test Workflow

1. **Browse Pets** (Adoption System)
   - Go to http://localhost:5000/pets/browse
   - View available pets from shelter

2. **Submit Application**
   - Login as adopter
   - Click on a pet
   - Click "Apply for Adoption"
   - Fill out the form

3. **Approve Application** (Shelter Staff)
   - Login as shelter staff
   - Go to dashboard
   - View pending applications
   - Approve an application

4. **View Health Records** (Adopter)
   - Login as adopter
   - Go to "My Pets"
   - View health information

5. **Schedule Appointment** (Veterinarian)
   - Login as vet
   - Go to appointments
   - Create new appointment

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Import Errors
```powershell
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

### Database Errors
```powershell
# Delete and recreate databases
python init_databases.py
```

## 📚 API Documentation

### Shelter System API

**Get All Pets**
```
GET http://localhost:5001/api/pets/
Parameters: species, breed, age, gender, page
```

**Get Pet Details**
```
GET http://localhost:5001/api/pets/{id}
```

**Add New Pet**
```
POST http://localhost:5001/api/pets/
Body: JSON with pet data
```

### Veterinary System API

**Get Health Record**
```
GET http://localhost:5002/api/health/{pet_id}
```

**Update Health Record**
```
POST http://localhost:5002/api/update-record/
Body: JSON with health data
```

**Schedule Appointment**
```
POST http://localhost:5002/api/schedule-appointment/
Body: JSON with appointment data
```

## 🎨 Customization

### Adding More Pets
1. Login as shelter staff
2. Go to http://localhost:5001/manage/pets/add
3. Fill in pet information
4. Submit

### Modifying Styles
- Edit templates in `*/templates/` folders
- Modify CSS in `base.html`
- Add custom styles in `*/static/css/`

## 📖 Project Structure
```
Vet-Management/
├── adoption_system/        # Main adoption platform
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── utils/
├── shelter_system/         # Shelter management
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   └── templates/
├── veterinary_system/      # Vet records & appointments
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   └── utils/
├── config.py               # Shared configuration
├── requirements.txt        # Python dependencies
├── init_databases.py       # Database setup script
└── README.md
```

## 🆘 Support

If you encounter issues:
1. Check the terminal output for error messages
2. Verify all three systems are running
3. Ensure virtual environment is activated
4. Check database files exist (*.db files)
5. Review `.env` configuration

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- Dog CEO API: https://dog.ceo/dog-api/
- The Cat API: https://thecatapi.com/

---

**Enjoy building your Pet Adoption System! 🐶🐱❤️**
