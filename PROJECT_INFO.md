# 🐾 Pet Adoption System - Complete Project Documentation

## 📋 Project Overview

The **Pet Adoption System** is a comprehensive web-based platform that connects animal shelters, pet adopters, and veterinary clinics. This three-system architecture enables:

- **Adopters** to browse and adopt pets online
- **Shelters** to manage their inventory and adoption processes
- **Veterinarians** to maintain health records and schedule appointments

## 🏗️ System Architecture

### Three Integrated Systems

```
┌─────────────────────┐
│  Adoption System    │ ← Main User Interface (Port 5000)
│  (Main Hub)         │
└──────────┬──────────┘
           │
           ├──────────────────────────────────┐
           │                                  │
           ▼                                  ▼
┌──────────────────────┐         ┌──────────────────────┐
│  Shelter System      │         │  Veterinary System   │
│  (Pet Management)    │         │  (Health Records)    │
│  Port 5001           │         │  Port 5002           │
└──────────────────────┘         └──────────────────────┘
```

### System Communication

- **REST APIs** for inter-system communication
- **External APIs**: Dog API, Cat API, Google Calendar API
- **Email System**: SMTP for notifications

## 📁 Project Structure

```
Vet-Management/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick start guide
├── 📄 PROJECT_INFO.md              # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 config.py                    # Shared configuration
├── 📄 .env                         # Environment variables
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 init_databases.py            # Database initialization
├── 📄 system_check.py              # System verification
├── 📄 start_all.py                 # Startup script
│
├── 📂 adoption_system/             # MAIN SYSTEM (Port 5000)
│   ├── 📄 app.py                   # Flask application
│   ├── 📄 models.py                # Database models
│   │
│   ├── 📂 routes/                  # Route handlers
│   │   ├── 📄 auth.py              # Authentication routes
│   │   ├── 📄 adoption.py          # Adoption management
│   │   ├── 📄 pets.py              # Pet browsing
│   │   └── 📄 profile.py           # User profiles
│   │
│   ├── 📂 templates/               # HTML templates
│   │   ├── 📄 base.html            # Base template
│   │   ├── 📄 index.html           # Home page
│   │   ├── 📂 auth/                # Auth templates
│   │   ├── 📂 pets/                # Pet templates
│   │   ├── 📂 adoption/            # Adoption templates
│   │   └── 📂 errors/              # Error pages
│   │
│   ├── 📂 static/                  # Static files
│   │   └── 📂 uploads/             # Uploaded files
│   │
│   └── 📂 utils/                   # Utility modules
│       ├── 📄 api_client.py        # API integrations
│       └── 📄 email_service.py     # Email handling
│
├── 📂 shelter_system/              # SHELTER SYSTEM (Port 5001)
│   ├── 📄 app.py                   # Flask application
│   ├── 📄 models.py                # Pet, Image, Log models
│   │
│   ├── 📂 routes/                  # Route handlers
│   │   ├── 📄 pets_api.py          # REST API endpoints
│   │   └── 📄 pets_management.py   # Management UI
│   │
│   ├── 📂 templates/               # HTML templates
│   │   ├── 📄 index.html
│   │   ├── 📄 dashboard.html
│   │   └── 📂 manage/              # Management pages
│   │
│   └── 📂 static/                  # Static files
│       └── 📂 uploads/             # Pet images
│
└── 📂 veterinary_system/           # VET SYSTEM (Port 5002)
    ├── 📄 app.py                   # Flask application
    ├── 📄 models.py                # Vet, Record, Appointment models
    │
    ├── 📂 routes/                  # Route handlers
    │   ├── 📄 health_api.py        # Health records API
    │   ├── 📄 appointments.py      # Appointment management
    │   └── 📄 vets.py              # Vet management
    │
    ├── 📂 templates/               # HTML templates
    │   ├── 📄 index.html
    │   ├── 📄 dashboard.html
    │   ├── 📂 appointments/
    │   └── 📂 vets/
    │
    ├── 📂 static/                  # Static files
    │
    └── 📂 utils/                   # Utility modules
        └── 📄 google_calendar.py   # Google Calendar API
```

## 🗄️ Database Schema

### Adoption System Database

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- adopter, shelter, vet
    phone VARCHAR(20),
    address TEXT,
    created_at DATETIME,
    updated_at DATETIME
);
```

#### Adoption Applications Table
```sql
CREATE TABLE adoption_applications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    pet_id INTEGER NOT NULL,
    pet_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    reason TEXT,
    experience TEXT,
    living_situation VARCHAR(100),
    has_yard BOOLEAN,
    other_pets TEXT,
    date_submitted DATETIME,
    date_reviewed DATETIME,
    reviewed_by INTEGER,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### Adopted Pets Table
```sql
CREATE TABLE adopted_pets (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    pet_name VARCHAR(100),
    adopter_id INTEGER NOT NULL,
    application_id INTEGER,
    adoption_date DATETIME,
    adoption_fee FLOAT,
    microchip_number VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (adopter_id) REFERENCES users(id)
);
```

### Shelter System Database

#### Pets Table
```sql
CREATE TABLE pets (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(20) NOT NULL,  -- dog, cat
    breed VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    color VARCHAR(50),
    size VARCHAR(20),  -- small, medium, large
    description TEXT,
    status VARCHAR(20) DEFAULT 'available',  -- available, adopted, pending
    vaccinated BOOLEAN,
    spayed_neutered BOOLEAN,
    microchipped BOOLEAN,
    special_needs TEXT,
    good_with_kids BOOLEAN,
    good_with_pets BOOLEAN,
    energy_level VARCHAR(20),
    intake_date DATETIME,
    adoption_fee FLOAT,
    created_at DATETIME,
    updated_at DATETIME
);
```

#### Pet Images Table
```sql
CREATE TABLE pet_images (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN,
    caption VARCHAR(200),
    uploaded_at DATETIME,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);
```

### Veterinary System Database

#### Vets Table
```sql
CREATE TABLE vets (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100),
    license_number VARCHAR(50),
    bio TEXT,
    created_at DATETIME
);
```

#### Vet Records Table
```sql
CREATE TABLE vet_records (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    pet_name VARCHAR(100),
    last_checkup DATETIME,
    weight FLOAT,
    temperature FLOAT,
    vaccinations TEXT,  -- JSON
    notes TEXT,
    medications TEXT,
    allergies TEXT,
    chronic_conditions TEXT,
    dental_health VARCHAR(50),
    heartworm_status VARCHAR(50),
    flea_tick_prevention BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME,
    updated_by INTEGER,
    FOREIGN KEY (updated_by) REFERENCES vets(id)
);
```

#### Appointments Table
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    pet_name VARCHAR(100),
    owner_name VARCHAR(100),
    owner_email VARCHAR(120),
    owner_phone VARCHAR(20),
    vet_id INTEGER NOT NULL,
    date DATETIME NOT NULL,
    duration INTEGER DEFAULT 30,
    reason VARCHAR(200),
    notes TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    google_calendar_event_id VARCHAR(200),
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (vet_id) REFERENCES vets(id)
);
```

## 🔌 API Documentation

### Shelter System API Endpoints

#### GET /api/pets/
Get all available pets with filtering
```
Parameters:
  - species: 'dog', 'cat', or 'all'
  - breed: string
  - age: integer
  - gender: 'male' or 'female'
  - status: 'available', 'adopted', 'pending'
  - search: search term
  - page: page number
  - per_page: items per page

Response:
{
  "pets": [...],
  "total": 50,
  "pages": 5,
  "current_page": 1
}
```

#### GET /api/pets/<id>
Get specific pet details
```
Response:
{
  "id": 1,
  "name": "Max",
  "species": "dog",
  "breed": "Golden Retriever",
  "age": 2,
  ...
}
```

#### POST /api/pets/
Add new pet to shelter
```
Body:
{
  "name": "Buddy",
  "species": "dog",
  "breed": "Labrador",
  "age": 3,
  "gender": "male",
  ...
}
```

### Veterinary System API Endpoints

#### GET /api/health/<pet_id>
Get health records for a pet
```
Response:
{
  "pet_id": 1,
  "pet_name": "Max",
  "last_checkup": "2025-01-15T10:00:00",
  "vaccinations": [...],
  ...
}
```

#### POST /api/update-record/
Update or create health record
```
Body:
{
  "pet_id": 1,
  "weight": 25.5,
  "temperature": 38.5,
  "vaccinations": [...],
  "notes": "Healthy checkup"
}
```

#### POST /api/schedule-appointment/
Schedule veterinary appointment
```
Body:
{
  "pet_id": 1,
  "vet_id": 1,
  "date": "2025-02-01T14:00:00",
  "reason": "Annual checkup",
  "owner_email": "owner@example.com"
}
```

## 🔐 User Roles & Permissions

### Adopter Role
- Browse available pets
- Submit adoption applications
- View own applications and adopted pets
- Access health records of adopted pets
- Schedule vet appointments for adopted pets

### Shelter Staff Role
- View all adoption applications
- Approve/reject applications
- Add/edit/delete pets in shelter
- Upload pet images
- Update pet status
- View shelter statistics

### Veterinarian Role
- View and update health records
- Manage appointments
- Add vaccinations
- Update medical information
- View appointment calendar

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0.23** - ORM
- **Flask-Login 0.6.3** - User session management
- **Flask-Mail 0.9.1** - Email handling
- **Flask-CORS 4.0.0** - Cross-origin requests

### Frontend
- **Bootstrap 5.3** - UI framework
- **Bootstrap Icons** - Icon library
- **JavaScript** - Client-side interactivity

### External APIs
- **Dog CEO API** - Dog breeds and images
- **The Cat API** - Cat breeds and information
- **Google Calendar API** - Appointment scheduling
- **SMTP** - Email notifications

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production ready (configurable)

## 🚀 Deployment Guide

### Local Development
```bash
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_databases.py

# Run
python start_all.py
```

### Production Deployment (Example with Heroku)

1. **Update database to PostgreSQL**
```python
# In .env
ADOPTION_DB_URI=postgresql://user:pass@host/adoption_db
```

2. **Create Procfile**
```
web: gunicorn adoption_system.app:app
worker1: gunicorn shelter_system.app:app
worker2: gunicorn veterinary_system.app:app
```

3. **Add requirements**
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

4. **Deploy**
```bash
heroku create your-app-name
git push heroku main
heroku run python init_databases.py
```

## 🔒 Security Considerations

### Implemented
- ✅ Password hashing (Werkzeug)
- ✅ CSRF protection (Flask-WTF)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Session management (Flask-Login)
- ✅ Input validation

### Recommended for Production
- [ ] HTTPS enforcement
- [ ] Rate limiting
- [ ] JWT tokens for API
- [ ] OAuth2 authentication
- [ ] File upload virus scanning
- [ ] Database encryption
- [ ] Environment variable encryption

## 📊 Feature Checklist

### Core Features
- ✅ User registration and authentication
- ✅ Pet browsing with filters
- ✅ Adoption application system
- ✅ Email notifications
- ✅ Health record management
- ✅ Appointment scheduling
- ✅ Multi-system integration
- ✅ REST APIs

### Advanced Features
- ✅ Image upload for pets
- ✅ Dog/Cat API integration
- ✅ Google Calendar sync
- ✅ Status tracking
- ✅ Activity logging

### Future Enhancements
- [ ] Pet care chatbot
- [ ] Real-time notifications (WebSocket)
- [ ] Payment integration (adoption fees)
- [ ] Mobile app (React Native)
- [ ] Social media sharing
- [ ] Pet matching algorithm
- [ ] Video consultations
- [ ] Donation system

## 🐛 Common Issues & Solutions

### Issue: Port already in use
```powershell
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Import errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: Database locked
```bash
# Close all connections and restart
python init_databases.py
```

### Issue: Templates not found
```bash
# Check directory structure
# Ensure templates folder exists in each system
```

## 📞 Support & Contact

For issues, questions, or contributions:
- Check the QUICKSTART.md for setup help
- Run system_check.py for diagnostics
- Review error logs in terminal output

## 📝 License

This is an educational project created for learning purposes.

---

**Built with ❤️ for pets and their future families**

🐶 🐱 🏠
