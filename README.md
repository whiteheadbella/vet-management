# Pet Adoption System - Comprehensive Platform

A complete pet adoption platform connecting shelters, adopters, and veterinary clinics.

## 🏗️ System Architecture

This project consists of three integrated systems:

1. **Adoption System (Main System)** - Port 5000
   - User management and authentication
   - Pet browsing and adoption requests
   - Email notifications
   - Integration hub

2. **Shelter Inventory System** - Port 5001
   - Pet management
   - Availability tracking
   - Image uploads
   - API provider for pet data

3. **Veterinary Management System** - Port 5002
   - Health records management
   - Appointment scheduling
   - Vaccination tracking
   - Medical history

## 🚀 Features

### Adoption System
- User registration/login (Adopters, Shelter Staff, Vets)
- Browse available pets (via Dog/Cat APIs)
- Submit adoption applications
- Email notifications
- View pet health records
- Schedule vet appointments
- **🤖 AI Chatbot Assistant** - Intelligent assistant that integrates data from both Shelter and Veterinary systems

### Shelter Inventory System
- Add/update pets
- Manage pet status (Available/Adopted)
- Upload pet images
- Expose REST API for pet data
- **🤖 Shelter Chatbot** - Query pet inventory, statistics, and availability using natural language

### Veterinary Management System
- Track pet health records
- Manage vaccinations
- Schedule appointments (Google Calendar integration)
- Update medical information
- **🤖 Veterinary Chatbot** - Check health records, appointments, and vet information through conversational interface

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **APIs**: 
  - Dog API (https://dog.ceo/dog-api/)
  - Cat API (https://thecatapi.com/)
  - Google Calendar API
  - Email (SMTP)

## 📦 Installation & Deployment

### 🐳 Quick Docker Deploy (Recommended)

**Prerequisites:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

```powershell
# One command to deploy everything:
.\deploy_docker.ps1
```

**That's it!** In 5 minutes you'll have:
- ✅ All 3 systems running
- ✅ 20 pets populated
- ✅ 20 health records
- ✅ 3 veterinarians
- ✅ 5 appointments

**Access at:**
- http://localhost:5000 (Adoption System)
- http://localhost:5001 (Shelter System)
- http://localhost:5002 (Veterinary System)

**Full Docker Guide:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

---

### 📝 Manual Setup (Development)

1. **Clone & Setup**
```bash
cd Vet-Management
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
copy .env.example .env
# Edit .env with your settings
```

3. **Initialize & Populate**
```bash
python init_databases.py
python populate_pets.py
python populate_vet_records.py
```

4. **Run All Systems**
```bash
# Terminal 1 - Adoption System
python adoption_system/app.py

# Terminal 2 - Shelter System
python shelter_system/app.py

# Terminal 3 - Veterinary System
python veterinary_system/app.py
```

## 🌐 System URLs

- **Adoption System**: http://localhost:5000
  - 🤖 **Chatbot**: http://localhost:5000/chatbot
- **Shelter System**: http://localhost:5001
  - 🤖 **Chatbot**: http://localhost:5001/chatbot
- **Veterinary System**: http://localhost:5002
  - 🤖 **Chatbot**: http://localhost:5002/chatbot

## 📊 Database Schema

### Adoption System
- users
- adoption_applications
- adopted_pets
- notifications

### Shelter Inventory System
- pets
- pet_images
- shelter_logs

### Veterinary Management System
- vets
- vet_records
- appointments

## 🔌 API Endpoints

### Adoption System APIs
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/pets` - Browse available pets
- `POST /api/adopt` - Submit adoption application
- `GET /api/health/<pet_id>` - Get pet health records

### Shelter System APIs
- `GET /api/pets/` - List all available pets
- `GET /api/pets/<id>` - Get pet details
- `POST /api/pets/` - Add new pet
- `PUT /api/update-status/` - Update pet status
- `POST /api/pets/<id>/images` - Upload pet images

### Veterinary System APIs
- `GET /api/health/<pet_id>` - Get health records
- `POST /api/update-record/` - Update health record
- `POST /api/schedule-appointment/` - Schedule appointment

## 🔐 User Roles

1. **Adopter**: Browse pets, submit adoption requests
2. **Shelter Staff**: Manage shelter inventory, approve adoptions
3. **Veterinarian**: Manage health records, schedule appointments

## 📧 Email Notifications

- Adoption request confirmation
- Application status updates
- Appointment reminders
- Health record updates

## 🐳 Docker Deployment (Recommended)

### Simple 3-Step Process:

**1. Install Docker Desktop** (one-time)
   - Download: https://www.docker.com/products/docker-desktop
   - Install and restart computer

**2. Deploy** (5 minutes)
   ```powershell
   .\deploy_docker.ps1
   ```

**3. Access** - Open in browser:
   - http://localhost:5000 (Adoption System)
   - http://localhost:5001 (Shelter System)
   - http://localhost:5002 (Veterinary System)

### Documentation:
- 📖 [Docker Quick Start](DOCKER_QUICK_START.md) - Simple step-by-step
- 📖 [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) - Complete reference
- 🔌 [API Testing Guide](POSTMAN_API_GUIDE.md) - Test integration

### Deployed System Includes
- ✅ 20 pets (10 dogs, 10 cats) with images
- ✅ 20 complete health records with vaccinations
- ✅ 3 veterinarians with profiles
- ✅ 5 scheduled appointments
- ✅ Full cross-system integration
- ✅ **3 AI Chatbot Assistants** with natural language processing

---

## 🤖 Chatbot Integration

Each system includes an intelligent chatbot assistant accessible from the footer or navigation bar.

### Chatbot Features

**🏠 Shelter Chatbot** (Purple theme)
- Query pet statistics and inventory
- Search pets by name, breed, or characteristics
- Check medical information (vaccinations, spay/neuter status)
- Find family-friendly pets
- View recent activity logs

**Sample Queries:**
```
"How many pets do we have?"
"Show me available dogs"
"Find Max"
"Pets good with kids"
"Vaccinated pets"
```

**🏥 Veterinary Chatbot** (Green theme)
- View health record statistics
- Check appointment schedules
- Search health records by pet ID
- List veterinarians and specializations
- Identify pets requiring medical attention

**Sample Queries:**
```
"How many health records?"
"Show upcoming appointments"
"Show available vets"
"Find record for pet 1"
"Today's appointments"
```

**❤️ Adoption Chatbot** (Pink theme) - **Integration Demo**
- Browse available pets from Shelter System API
- Check pet health status from Veterinary System API
- **Combines data from both systems in real-time**
- Explain adoption process and requirements
- Filter pets by characteristics

**Sample Queries:**
```
"Show me available pets"
"Check health status for pet 1"  ← Cross-system integration!
"Dogs for adoption"
"How to adopt?"
"Pets good with kids"
```

### Integration Architecture

The Adoption chatbot demonstrates **true microservices integration**:

```python
# Fetches pet info from Shelter System
GET http://localhost:5001/api/pets/1

# Fetches health info from Veterinary System  
GET http://localhost:5002/api/health/1

# Combines responses into unified answer
```

**Access Chatbots:**
- Click the footer button on any system homepage
- Or navigate directly to `/chatbot` on each system
- Or use quick action buttons for common queries

**Documentation:**
- 📖 [Chatbot Quick Start](CHATBOT_QUICKSTART.md)
- 📖 [Complete Chatbot Guide](CHATBOT_GUIDE.md)

---

## 🤝 Contributing

This is an educational project for veterinary management system development.

## 📝 License

Educational Project - 2025

## 👥 Target Users

- Pet Adopters
- Animal Shelters
- Veterinary Clinics
- Animal Welfare Groups
- Volunteers

---

## 🎓 For Students & Presenters

**Pre-Presentation Checklist:**
- [ ] Choose deployment method (Docker/Render/Local)
- [ ] Run deployment script
- [ ] Test all 3 systems
- [ ] Generate QR codes for mobile access
- [ ] Test API endpoints in Postman
- [ ] Prepare backup deployment
- [ ] Test on multiple devices

**Demo Flow (7 minutes):**
1. Browse pets with filters → Show integration
2. View health records → Show vaccination tracking
3. Schedule appointment → Show cross-system communication
4. **🤖 Chatbot Integration Demo** → Ask "Check health status for pet 1" in Adoption chatbot
5. View veterinarian profiles → Show complete system
6. Test APIs in Postman → Show technical architecture

**Chatbot Demo (Recommended):**
1. Open Adoption chatbot: http://localhost:5000/chatbot
2. Query: "Show me available pets" (calls Shelter API)
3. Query: "Check health status for pet 1" (calls BOTH Shelter + Vet APIs)
4. Explain: Real-time microservices integration via REST APIs
