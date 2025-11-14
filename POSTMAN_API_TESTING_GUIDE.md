# 🔌 Postman API Testing Guide

## Complete Guide to Test System Integration with Postman

---

## ✅ Prerequisites

1. **All 3 servers must be running:**
   ```powershell
   .\start_all_servers.ps1
   ```

2. **Postman installed:**
   - Download from: https://www.postman.com/downloads/
   - Or use Postman Web: https://web.postman.com/

3. **Sample data populated:**
   ```powershell
   python populate_pets.py
   python populate_vet_records.py
   ```

---

## 🌐 System Architecture Overview

```
┌─────────────────────┐
│ Adoption System     │  Port 5000
│ (Public Interface)  │  Calls APIs from Shelter & Vet systems
└─────────────────────┘
          │
          ├──────────────┐
          ▼              ▼
┌─────────────────┐  ┌─────────────────┐
│ Shelter System  │  │ Vet System      │
│ (Pet Database)  │  │ (Health Records)│
│ Port 5001       │  │ Port 5002       │
│                 │  │                 │
│ Provides:       │  │ Provides:       │
│ - Pet List      │  │ - Health Data   │
│ - Pet Details   │  │ - Appointments  │
│ - Pet Images    │  │ - Vaccinations  │
└─────────────────┘  └─────────────────┘
```

---

## 📋 API ENDPOINTS - COMPLETE LIST

### 🏠 SHELTER SYSTEM (Port 5001)

#### 1. Get All Pets
- **URL:** `http://localhost:5001/api/pets/`
- **Method:** GET
- **Description:** Retrieve all pets with optional filters
- **Query Parameters:**
  - `species` - dog/cat/all (default: all)
  - `breed` - filter by breed
  - `age` - filter by age
  - `gender` - male/female
  - `status` - available/pending/adopted
  - `search` - search in name/description
  - `page` - page number (default: 1)
  - `per_page` - items per page (default: 12)

#### 2. Get Single Pet
- **URL:** `http://localhost:5001/api/pets/{pet_id}`
- **Method:** GET
- **Description:** Get detailed information about a specific pet
- **Example:** `http://localhost:5001/api/pets/1`

#### 3. Add New Pet
- **URL:** `http://localhost:5001/api/pets/`
- **Method:** POST
- **Description:** Add a new pet to the shelter system
- **Body (JSON):**
```json
{
  "name": "Buddy",
  "species": "dog",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "male",
  "description": "Friendly and energetic",
  "status": "available",
  "medical_info": "Up to date on vaccinations",
  "behavioral_traits": "Good with kids, loves to play fetch"
}
```

#### 4. Update Pet Status
- **URL:** `http://localhost:5001/api/pets/{pet_id}/status`
- **Method:** PUT
- **Body (JSON):**
```json
{
  "status": "adopted"
}
```

#### 5. Get Pet Statistics
- **URL:** `http://localhost:5001/api/pets/statistics`
- **Method:** GET
- **Description:** Get overall shelter statistics

#### 6. Get Pet Images
- **URL:** `http://localhost:5001/api/pets/{pet_id}/images`
- **Method:** GET
- **Description:** Get all images for a specific pet

#### 7. Upload Pet Image
- **URL:** `http://localhost:5001/api/pets/{pet_id}/images`
- **Method:** POST
- **Body (JSON):**
```json
{
  "image_url": "https://example.com/image.jpg",
  "caption": "Playing in the park",
  "is_primary": false
}
```

#### 8. Get Shelter Activity Logs
- **URL:** `http://localhost:5001/api/logs/`
- **Method:** GET
- **Query Parameters:**
  - `pet_id` - filter by specific pet
  - `limit` - number of logs (default: 50)

---

### 🏥 VETERINARY SYSTEM (Port 5002)

#### 1. Get Pet Health Record
- **URL:** `http://localhost:5002/api/health/{pet_id}`
- **Method:** GET
- **Description:** Get health records for a specific pet
- **Example:** `http://localhost:5002/api/health/1`

#### 2. Create Health Record
- **URL:** `http://localhost:5002/api/health/`
- **Method:** POST
- **Body (JSON):**
```json
{
  "pet_id": 1,
  "weight": 25.5,
  "temperature": 101.2,
  "vaccinations": "Rabies, Distemper, Parvo",
  "medications": "Heartworm prevention",
  "notes": "Healthy, regular checkup",
  "last_checkup": "2024-11-14",
  "next_checkup": "2025-02-14",
  "vet_id": 1
}
```

#### 3. Update Health Record
- **URL:** `http://localhost:5002/api/update-record/`
- **Method:** POST or PUT
- **Body (JSON):**
```json
{
  "pet_id": 1,
  "weight": 26.0,
  "temperature": 101.5,
  "notes": "Slight weight gain, healthy"
}
```

#### 4. Add Vaccination Record
- **URL:** `http://localhost:5002/api/health/{pet_id}/vaccinations`
- **Method:** POST
- **Body (JSON):**
```json
{
  "vaccination_name": "Rabies",
  "date_administered": "2024-11-14",
  "next_due_date": "2025-11-14",
  "administered_by": "Dr. Sarah Smith"
}
```

#### 5. Get All Health Records
- **URL:** `http://localhost:5002/api/records`
- **Method:** GET
- **Query Parameters:**
  - `vet_id` - filter by veterinarian
  - `limit` - number of records

#### 6. Get Veterinary Statistics
- **URL:** `http://localhost:5002/api/stats`
- **Method:** GET
- **Description:** Overall system statistics

#### 7. Schedule Appointment
- **URL:** `http://localhost:5002/api/schedule-appointment/`
- **Method:** POST
- **Body (JSON):**
```json
{
  "pet_id": 1,
  "vet_id": 1,
  "appointment_date": "2024-11-20 10:00:00",
  "reason": "Annual checkup",
  "notes": "Bring vaccination records"
}
```

#### 8. Get Pet Appointments
- **URL:** `http://localhost:5002/api/appointments/{pet_id}`
- **Method:** GET
- **Description:** Get all appointments for a specific pet

#### 9. Get All Veterinarians
- **URL:** `http://localhost:5002/api/vets`
- **Method:** GET
- **Description:** List all veterinarians in the system

---

### 🐾 ADOPTION SYSTEM (Port 5000)

#### 1. Get Pet Health (Integrated)
- **URL:** `http://localhost:5000/api/health/{pet_id}`
- **Method:** GET
- **Description:** This calls Vet System API internally
- **Example:** `http://localhost:5000/api/health/1`

---

## 🚀 STEP-BY-STEP POSTMAN TESTING

### STEP 1: Create New Collection

1. Open Postman
2. Click "New" → "Collection"
3. Name it: **"Pet Management System APIs"**
4. Click "Create"

---

### STEP 2: Set Up Environment Variables (Optional but Recommended)

1. Click "Environments" (left sidebar)
2. Click "+" to create new environment
3. Name it: **"Local Development"**
4. Add variables:
   - `shelter_base_url` = `http://localhost:5001`
   - `vet_base_url` = `http://localhost:5002`
   - `adoption_base_url` = `http://localhost:5000`
5. Click "Save"
6. Select this environment from the dropdown (top right)

---

### STEP 3: Test Integration - Real-World Scenario

#### Scenario: Browse Pet → View Details → See Health Records

**Request 1: Get All Available Pets**

1. Click "Add request" in your collection
2. Name: **"Get All Pets"**
3. Method: **GET**
4. URL: `http://localhost:5001/api/pets/?status=available`
5. Click **Send**

**Expected Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "name": "Max",
      "species": "dog",
      "breed": "Golden Retriever",
      "age": 3,
      "gender": "male",
      "status": "available",
      "description": "Friendly and energetic dog",
      "created_at": "2024-11-14T10:30:00",
      "images": [
        {
          "id": 1,
          "image_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg",
          "is_primary": true
        }
      ]
    },
    // ... more pets
  ],
  "total": 20,
  "pages": 2,
  "current_page": 1
}
```

**Request 2: Get Specific Pet Details**

1. From previous response, copy a `pet_id` (e.g., 1)
2. Create new request: **"Get Pet Details"**
3. Method: **GET**
4. URL: `http://localhost:5001/api/pets/1`
5. Click **Send**

**Expected Response:**
```json
{
  "id": 1,
  "name": "Max",
  "species": "dog",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "male",
  "status": "available",
  "description": "Friendly and energetic dog",
  "medical_info": "Vaccinated, neutered, microchipped",
  "behavioral_traits": "Good with children, house trained",
  "created_at": "2024-11-14T10:30:00",
  "updated_at": "2024-11-14T10:30:00",
  "images": [
    {
      "id": 1,
      "image_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg",
      "caption": "Max playing fetch",
      "is_primary": true,
      "uploaded_at": "2024-11-14T10:30:00"
    }
  ]
}
```

**Request 3: Get Pet Health Records (INTEGRATION TEST)**

1. Create new request: **"Get Pet Health Records"**
2. Method: **GET**
3. URL: `http://localhost:5002/api/health/1`
4. Click **Send**

**Expected Response:**
```json
{
  "pet_id": 1,
  "weight": 25.5,
  "temperature": 101.2,
  "vaccinations": "Rabies (2024-01-15), Distemper (2024-01-15), Parvo (2024-01-15)",
  "medications": "Heartworm prevention (monthly)",
  "allergies": "None",
  "notes": "Healthy dog, regular checkups",
  "last_checkup": "2024-10-15",
  "next_checkup": "2025-01-15",
  "vet_name": "Dr. Sarah Smith",
  "vet_specialization": "General Practice",
  "created_at": "2024-11-14T10:35:00",
  "updated_at": "2024-11-14T10:35:00"
}
```

✅ **This proves the integration works!** The Adoption System can get pet data from Shelter System, and health data from Vet System.

---

### STEP 4: Test Full CRUD Operations

#### CREATE: Add New Pet

1. Create new request: **"Add New Pet"**
2. Method: **POST**
3. URL: `http://localhost:5001/api/pets/`
4. Go to **Body** tab
5. Select **raw** and **JSON**
6. Paste:
```json
{
  "name": "Charlie",
  "species": "dog",
  "breed": "Beagle",
  "age": 2,
  "gender": "male",
  "description": "Sweet and curious beagle puppy",
  "status": "available",
  "medical_info": "All vaccinations current",
  "behavioral_traits": "Friendly, loves treats"
}
```
7. Click **Send**

**Expected Response:**
```json
{
  "message": "Pet added successfully",
  "pet": {
    "id": 21,
    "name": "Charlie",
    "species": "dog",
    "breed": "Beagle",
    "age": 2,
    "status": "available"
  }
}
```

#### READ: Verify Pet Was Added

1. Create new request: **"Get Charlie"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/21` (use ID from previous response)
4. Click **Send**

#### UPDATE: Change Pet Status

1. Create new request: **"Update Pet Status"**
2. Method: **PUT**
3. URL: `http://localhost:5001/api/pets/21/status`
4. Body (JSON):
```json
{
  "status": "pending"
}
```
5. Click **Send**

#### CREATE: Add Health Record for New Pet

1. Create new request: **"Add Health Record"**
2. Method: **POST**
3. URL: `http://localhost:5002/api/health/`
4. Body (JSON):
```json
{
  "pet_id": 21,
  "weight": 18.5,
  "temperature": 101.0,
  "vaccinations": "Rabies, Distemper",
  "medications": "None",
  "notes": "Initial health check - good condition",
  "last_checkup": "2024-11-14",
  "next_checkup": "2025-02-14",
  "vet_id": 1
}
```
5. Click **Send**

#### VERIFY INTEGRATION: Get Health from Vet System

1. Create new request: **"Get Charlie's Health"**
2. Method: **GET**
3. URL: `http://localhost:5002/api/health/21`
4. Click **Send**
5. Should return the health record you just created!

---

### STEP 5: Test Appointment Scheduling

#### Schedule Veterinary Appointment

1. Create new request: **"Schedule Appointment"**
2. Method: **POST**
3. URL: `http://localhost:5002/api/schedule-appointment/`
4. Body (JSON):
```json
{
  "pet_id": 1,
  "vet_id": 1,
  "appointment_date": "2024-11-20 10:00:00",
  "reason": "Annual checkup",
  "notes": "Routine examination"
}
```
5. Click **Send**

**Expected Response:**
```json
{
  "message": "Appointment scheduled successfully",
  "appointment": {
    "id": 6,
    "pet_id": 1,
    "vet_id": 1,
    "appointment_date": "2024-11-20 10:00:00",
    "reason": "Annual checkup",
    "status": "scheduled"
  }
}
```

#### Get Pet Appointments

1. Create new request: **"Get Pet Appointments"**
2. Method: **GET**
3. URL: `http://localhost:5002/api/appointments/1`
4. Click **Send**

---

### STEP 6: Test Filtering and Search

#### Filter by Species

1. Create new request: **"Get All Dogs"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/?species=dog`
4. Click **Send**

#### Filter by Breed

1. Create new request: **"Get Golden Retrievers"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/?breed=Golden Retriever`
4. Click **Send**

#### Search by Name

1. Create new request: **"Search for Max"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/?search=Max`
4. Click **Send**

#### Multiple Filters

1. Create new request: **"Available Female Cats"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/?species=cat&gender=female&status=available`
4. Click **Send**

---

### STEP 7: Test Statistics Endpoints

#### Shelter Statistics

1. Create new request: **"Shelter Stats"**
2. Method: **GET**
3. URL: `http://localhost:5001/api/pets/statistics`
4. Click **Send**

**Expected Response:**
```json
{
  "total_pets": 21,
  "available": 18,
  "pending": 2,
  "adopted": 1,
  "dogs": 11,
  "cats": 10
}
```

#### Veterinary Statistics

1. Create new request: **"Vet Stats"**
2. Method: **GET**
3. URL: `http://localhost:5002/api/stats`
4. Click **Send**

**Expected Response:**
```json
{
  "total_vets": 3,
  "total_health_records": 21,
  "scheduled_appointments": 6,
  "completed_appointments": 0
}
```

---

## 🔗 INTEGRATION FLOW TESTING

### Flow 1: New Pet Adoption Process

```
1. POST /api/pets/           (Shelter) → Add pet
2. POST /api/health/         (Vet)     → Create health record
3. GET  /api/pets/          (Shelter) → View on adoption site
4. GET  /api/health/{id}    (Vet)     → Display health info
5. PUT  /api/pets/{id}/status (Shelter) → Mark as pending
6. POST /api/schedule-appointment/ (Vet) → Schedule checkup
```

### Flow 2: Browse Pets with Health Info

```
1. GET /api/pets/?status=available (Shelter) → Get available pets
2. For each pet:
   GET /api/health/{pet_id} (Vet) → Get health records
3. Display combined data on adoption site
```

---

## 📊 POSTMAN COLLECTION EXPORT

### Save Your Tests

1. Click the 3 dots (•••) next to your collection
2. Select "Export"
3. Choose "Collection v2.1"
4. Save as: `Pet_Management_APIs.postman_collection.json`

### Share with Team

1. Export the collection
2. Share the JSON file
3. Team members can import: File → Import → Choose file

---

## 🧪 TESTING CHECKLIST

### Basic API Tests
- [ ] Get all pets
- [ ] Get single pet by ID
- [ ] Add new pet
- [ ] Update pet status
- [ ] Get pet health record
- [ ] Create health record
- [ ] Schedule appointment

### Integration Tests
- [ ] Pet data flows from Shelter to Adoption system
- [ ] Health data flows from Vet to Adoption system
- [ ] Updating pet status reflects across systems
- [ ] New pets get health records assigned

### Filter Tests
- [ ] Filter by species
- [ ] Filter by breed
- [ ] Filter by age
- [ ] Filter by gender
- [ ] Filter by status
- [ ] Search by name

### Error Handling
- [ ] Non-existent pet ID returns 404
- [ ] Missing required fields returns 400
- [ ] Invalid data types handled gracefully

---

## ⚠️ COMMON ISSUES

### Issue 1: Connection Refused
**Error:** `Error: connect ECONNREFUSED 127.0.0.1:5001`

**Solution:**
```powershell
# Make sure all servers are running
.\start_all_servers.ps1

# Verify servers are up
Get-Process python
```

### Issue 2: No Data Returned
**Error:** `{"pets": [], "total": 0}`

**Solution:**
```powershell
# Populate databases
python populate_pets.py
python populate_vet_records.py
```

### Issue 3: CORS Errors
**Note:** CORS is already configured in the project! If you see CORS errors in browser but not in Postman, that's normal. Postman bypasses CORS.

### Issue 4: 404 Not Found
**Check:**
- URL is correct (check port numbers)
- Pet ID exists
- API endpoint path is correct

---

## 📈 ADVANCED: Postman Tests & Automation

### Add Tests to Requests

Click the "Tests" tab in any request and add:

```javascript
// Test 1: Status code is 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test 2: Response has correct structure
pm.test("Response has pets array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('pets');
});

// Test 3: Save pet ID for next request
var jsonData = pm.response.json();
if (jsonData.pets && jsonData.pets.length > 0) {
    pm.environment.set("pet_id", jsonData.pets[0].id);
}
```

### Run Collection with Tests

1. Click "Runner" (top left)
2. Select your collection
3. Click "Run Pet Management System APIs"
4. View test results

---

## 🎯 QUICK REFERENCE

### Base URLs
```
Adoption:  http://localhost:5000
Shelter:   http://localhost:5001
Vet:       http://localhost:5002
```

### Common Endpoints
```
GET    /api/pets/                  - List all pets
GET    /api/pets/{id}              - Get pet details
POST   /api/pets/                  - Add new pet
PUT    /api/pets/{id}/status       - Update status
GET    /api/health/{pet_id}        - Get health records
POST   /api/health/                - Create health record
POST   /api/schedule-appointment/  - Schedule appointment
```

### Sample Pet IDs (after populate_pets.py)
- Pet 1: Max (Dog)
- Pet 2: Buddy (Dog)
- Pet 11: Luna (Cat)
- Pet 12: Whiskers (Cat)

---

## 🎉 SUCCESS CRITERIA

You've successfully tested the integration when:
- ✅ You can get pet data from Shelter System
- ✅ You can get health data from Vet System
- ✅ Adding a pet in Shelter makes it available in Adoption
- ✅ Adding health records links to the correct pet
- ✅ Filtering and search work correctly
- ✅ Statistics endpoints return correct counts
- ✅ All CRUD operations work

---

## 📚 ADDITIONAL RESOURCES

- **Full API Documentation:** See `PROJECT_REPORT.md`
- **System Architecture:** See `README.md`
- **Troubleshooting:** See `TROUBLESHOOTING.md`
- **Deployment:** See `RENDER_DEPLOYMENT_GUIDE.md`

---

**Happy API Testing!** 🚀
