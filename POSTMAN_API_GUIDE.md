# Pet Adoption System - API Integration Guide for Postman

## 🔗 System Integration Overview

The Pet Adoption System consists of three interconnected microservices:

1. **Adoption System (Port 5000)** - Main hub that coordinates between systems
2. **Shelter System (Port 5001)** - Manages pet inventory and provides pet data
3. **Veterinary System (Port 5002)** - Manages health records and appointments

### Integration Flow Diagram

```
┌─────────────────────┐
│  Adoption System    │ (Port 5000)
│  (Coordinator)      │
└──────────┬──────────┘
           │
           ├─────────────────┐
           │                 │
           ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│ Shelter System   │  │ Veterinary System│
│ (Pet Data)       │  │ (Health Records) │
│ Port 5001        │  │ Port 5002        │
└──────────────────┘  └──────────────────┘
```

### How Integration Works

**Example User Journey:**
1. User browses pets on **Adoption System** → Calls **Shelter System** API
2. User views pet health info → **Adoption System** calls **Veterinary System** API
3. User adopts pet → **Adoption System** updates status in **Shelter System**
4. User schedules vet appointment → **Adoption System** calls **Veterinary System** API

---

## 📋 Postman Collection Setup

### Base URLs
- Adoption System: `http://localhost:5000`
- Shelter System: `http://localhost:5001`
- Veterinary System: `http://localhost:5002`

### Environment Variables (Create in Postman)
```json
{
  "adoption_url": "http://localhost:5000",
  "shelter_url": "http://localhost:5001",
  "veterinary_url": "http://localhost:5002"
}
```

---

## 🐾 SHELTER SYSTEM APIs (Port 5001)

### 1. Get All Available Pets
**Description:** Retrieve list of pets available for adoption

```
GET {{shelter_url}}/api/pets/
```

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| species | string | Filter by species | `dog`, `cat`, `all` |
| breed | string | Filter by breed | `Labrador` |
| age | integer | Filter by age | `2` |
| gender | string | Filter by gender | `male`, `female` |
| status | string | Filter by status | `available`, `adopted`, `all` |
| search | string | Search in name/description | `Max` |
| page | integer | Page number | `1` |
| per_page | integer | Results per page | `12` |

**Example Request:**
```bash
curl -X GET "http://localhost:5001/api/pets/?species=dog&status=available&page=1&per_page=10"
```

**Example Response:**
```json
{
  "pets": [
    {
      "id": 1,
      "name": "Max",
      "species": "dog",
      "breed": "Labrador Retriever",
      "age": 2,
      "gender": "male",
      "color": "Golden",
      "size": "large",
      "status": "available",
      "description": "Friendly and energetic",
      "image_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_123.jpg",
      "activity_level": "high",
      "barking_level": "moderate",
      "good_with_dogs": true,
      "good_with_cats": false,
      "trainability": "high",
      "created_at": "2025-11-14T10:00:00"
    }
  ],
  "total": 10,
  "pages": 1,
  "current_page": 1,
  "per_page": 10
}
```

---

### 2. Get Specific Pet Details
**Description:** Get detailed information about a specific pet

```
GET {{shelter_url}}/api/pets/{{pet_id}}
```

**Example Request:**
```bash
curl -X GET "http://localhost:5001/api/pets/1"
```

**Example Response:**
```json
{
  "id": 1,
  "name": "Max",
  "species": "dog",
  "breed": "Labrador Retriever",
  "age": 2,
  "gender": "male",
  "color": "Golden",
  "size": "large",
  "status": "available",
  "description": "Friendly and energetic dog, loves playing fetch",
  "image_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_123.jpg",
  "activity_level": "high",
  "barking_level": "moderate",
  "coat_type": "short",
  "shedding": "moderate",
  "trainability": "high",
  "good_with_dogs": true,
  "good_with_cats": false,
  "characteristics": ["Friendly", "Energetic", "Intelligent"],
  "adoption_fee": 200.00,
  "vaccinated": true,
  "spayed_neutered": true,
  "created_at": "2025-11-14T10:00:00",
  "updated_at": "2025-11-14T10:00:00"
}
```

---

### 3. Add New Pet
**Description:** Add a new pet to the shelter (Shelter staff only)

```
POST {{shelter_url}}/api/pets/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Bella",
  "species": "dog",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "female",
  "color": "Golden",
  "size": "large",
  "description": "Sweet and gentle dog",
  "activity_level": "moderate",
  "barking_level": "low",
  "good_with_dogs": true,
  "good_with_cats": true,
  "trainability": "high",
  "adoption_fee": 250.00
}
```

**Example Response:**
```json
{
  "message": "Pet added successfully",
  "pet": {
    "id": 21,
    "name": "Bella",
    "species": "dog",
    "status": "available"
  }
}
```

---

### 4. Update Pet Status
**Description:** Update pet status (available → adopted)

```
PUT {{shelter_url}}/api/update-status/
Content-Type: application/json
```

**Request Body:**
```json
{
  "pet_id": 1,
  "status": "adopted"
}
```

**Example Response:**
```json
{
  "message": "Pet status updated successfully",
  "pet_id": 1,
  "new_status": "adopted"
}
```

---

## 🏥 VETERINARY SYSTEM APIs (Port 5002)

### 5. Get Pet Health Record
**Description:** Retrieve complete health record for a pet

```
GET {{veterinary_url}}/api/health/{{pet_id}}
```

**Example Request:**
```bash
curl -X GET "http://localhost:5002/api/health/1"
```

**Example Response:**
```json
{
  "id": 1,
  "pet_id": 1,
  "pet_name": "Max",
  "species": "dog",
  "breed": "Labrador Retriever",
  "weight": 65.5,
  "temperature": 101.2,
  "heart_rate": 90,
  "respiratory_rate": 25,
  "body_condition_score": 5,
  "last_checkup": "2025-11-01T10:00:00",
  "vaccinations": [
    {
      "vaccine_name": "DHPP",
      "date_administered": "2025-10-01",
      "dose_number": 1,
      "manufacturer": "Zoetis",
      "lot_number": "DHPP-2025-001",
      "administered_by": "Dr. Sarah Johnson",
      "next_due_date": "2026-10-01"
    },
    {
      "vaccine_name": "Rabies",
      "date_administered": "2025-10-01",
      "dose_number": 1,
      "manufacturer": "Merial",
      "lot_number": "RAB-2025-456",
      "administered_by": "Dr. Sarah Johnson",
      "next_due_date": "2028-10-01"
    }
  ],
  "deworming_records": [
    {
      "date": "2025-09-15",
      "product": "Heartgard Plus",
      "administered_by": "Dr. Sarah Johnson"
    }
  ],
  "medications": "None currently",
  "allergies": "None known",
  "chronic_conditions": "None",
  "medical_history": "Routine checkups, no major issues",
  "surgical_history": "Neutered in 2024",
  "microchip_number": "982000123456789",
  "spay_neuter_date": "2024-01-15",
  "heartworm_status": "negative",
  "heartworm_test_date": "2025-10-01",
  "flea_tick_prevention": true,
  "flea_tick_product": "Frontline Plus",
  "dental_health": "Good",
  "dental_cleaning_date": "2025-08-01",
  "owner_name": "John Doe",
  "owner_phone": "555-0123",
  "owner_email": "john@example.com",
  "updated_by": 1,
  "updated_at": "2025-11-14T10:00:00"
}
```

---

### 6. Create Health Record
**Description:** Create a new health record for a pet

```
POST {{veterinary_url}}/api/health/
Content-Type: application/json
```

**Request Body:**
```json
{
  "pet_id": 21,
  "pet_name": "Bella",
  "species": "dog",
  "breed": "Golden Retriever",
  "weight": 60.0,
  "temperature": 101.5,
  "heart_rate": 85,
  "respiratory_rate": 22,
  "body_condition_score": 5,
  "vaccinations": [
    {
      "vaccine_name": "DHPP",
      "date_administered": "2025-11-01",
      "dose_number": 1,
      "administered_by": "Dr. Sarah Johnson",
      "next_due_date": "2026-11-01"
    }
  ],
  "owner_name": "Jane Smith",
  "owner_phone": "555-0456",
  "owner_email": "jane@example.com",
  "vet_id": 1
}
```

**Example Response:**
```json
{
  "message": "Health record created successfully",
  "record_id": 21,
  "pet_id": 21,
  "pet_name": "Bella"
}
```

---

### 7. Update Health Record
**Description:** Update existing health record

```
POST {{veterinary_url}}/api/update-record/
Content-Type: application/json
```

**Request Body:**
```json
{
  "pet_id": 1,
  "weight": 66.0,
  "temperature": 101.3,
  "notes": "Annual checkup completed. Pet is healthy.",
  "medications": "Heartgard Plus (monthly)",
  "dental_health": "Excellent"
}
```

**Example Response:**
```json
{
  "message": "Health record updated successfully",
  "pet_id": 1
}
```

---

### 8. Schedule Appointment
**Description:** Schedule a veterinary appointment

```
POST {{veterinary_url}}/api/schedule-appointment/
Content-Type: application/json
```

**Request Body:**
```json
{
  "pet_id": 1,
  "pet_name": "Max",
  "owner_name": "John Doe",
  "owner_phone": "555-0123",
  "owner_email": "john@example.com",
  "vet_id": 1,
  "date": "2025-11-20",
  "time": "10:00",
  "duration": 30,
  "reason": "vaccination",
  "notes": "Annual vaccination booster"
}
```

**Example Response:**
```json
{
  "message": "Appointment scheduled successfully",
  "appointment_id": 6,
  "date": "2025-11-20",
  "time": "10:00",
  "vet_name": "Dr. Sarah Johnson",
  "calendar_event_id": "abc123xyz"
}
```

---

### 9. Get Pet Appointments
**Description:** Get all appointments for a specific pet

```
GET {{veterinary_url}}/api/appointments/{{pet_id}}
```

**Example Response:**
```json
{
  "pet_id": 1,
  "appointments": [
    {
      "id": 6,
      "date": "2025-11-20",
      "time": "10:00:00",
      "duration": 30,
      "reason": "vaccination",
      "status": "scheduled",
      "vet_id": 1,
      "vet_name": "Dr. Sarah Johnson",
      "notes": "Annual vaccination booster"
    }
  ],
  "total": 1
}
```

---

### 10. Get Available Veterinarians
**Description:** Get list of all veterinarians

```
GET {{veterinary_url}}/api/vets
```

**Example Response:**
```json
{
  "vets": [
    {
      "id": 1,
      "name": "Dr. Sarah Johnson",
      "specialization": "General Practice",
      "email": "sarah.johnson@vetclinic.com",
      "phone": "555-0101",
      "license_number": "VET-2020-1234",
      "bio": "15 years of experience in small animal medicine"
    },
    {
      "id": 2,
      "name": "Dr. Michael Chen",
      "specialization": "Surgery",
      "email": "michael.chen@vetclinic.com",
      "phone": "555-0102"
    }
  ],
  "total": 3
}
```

---

## 🏠 ADOPTION SYSTEM APIs (Port 5000)

### 11. Get Breeds by Species
**Description:** Get available breeds for a species (uses external Dog/Cat APIs)

```
GET {{adoption_url}}/api/breeds/{{species}}
```

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/breeds/dog"
```

**Example Response:**
```json
{
  "species": "dog",
  "breeds": [
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "Bulldog",
    "Beagle"
  ]
}
```

---

## 🔄 Integration Test Scenarios

### Scenario 1: Complete Adoption Workflow

#### Step 1: Browse Available Pets (Adoption → Shelter)
```bash
# Adoption System fetches pets from Shelter System
GET http://localhost:5001/api/pets/?species=dog&status=available
```

#### Step 2: View Pet Health Records (Adoption → Veterinary)
```bash
# Adoption System fetches health records from Veterinary System
GET http://localhost:5002/api/health/1
```

#### Step 3: Adopt Pet - Update Status (Adoption → Shelter)
```bash
# Adoption System updates pet status in Shelter System
PUT http://localhost:5001/api/update-status/
Content-Type: application/json

{
  "pet_id": 1,
  "status": "adopted"
}
```

#### Step 4: Schedule Follow-up Appointment (Adoption → Veterinary)
```bash
# Adoption System schedules appointment in Veterinary System
POST http://localhost:5002/api/schedule-appointment/
Content-Type: application/json

{
  "pet_id": 1,
  "pet_name": "Max",
  "owner_name": "John Doe",
  "owner_phone": "555-0123",
  "owner_email": "john@example.com",
  "vet_id": 1,
  "date": "2025-11-25",
  "time": "14:00",
  "duration": 30,
  "reason": "checkup"
}
```

---

### Scenario 2: Add New Pet with Health Records

#### Step 1: Add Pet to Shelter
```bash
POST http://localhost:5001/api/pets/
Content-Type: application/json

{
  "name": "Charlie",
  "species": "cat",
  "breed": "Persian",
  "age": 1,
  "gender": "male",
  "color": "White",
  "size": "medium",
  "description": "Beautiful Persian cat"
}
```

**Response:** `{ "id": 22, ... }`

#### Step 2: Create Health Record
```bash
POST http://localhost:5002/api/health/
Content-Type: application/json

{
  "pet_id": 22,
  "pet_name": "Charlie",
  "species": "cat",
  "breed": "Persian",
  "weight": 10.5,
  "temperature": 101.0,
  "vaccinations": [
    {
      "vaccine_name": "FVRCP",
      "date_administered": "2025-11-01",
      "dose_number": 1
    }
  ],
  "vet_id": 1
}
```

---

### Scenario 3: Update Health After Appointment

#### Step 1: Get Appointment Details
```bash
GET http://localhost:5002/api/appointments/1
```

#### Step 2: Update Health Record After Visit
```bash
POST http://localhost:5002/api/update-record/
Content-Type: application/json

{
  "pet_id": 1,
  "weight": 66.5,
  "temperature": 101.2,
  "notes": "Completed vaccination. Pet is healthy and active.",
  "medications": "Heartgard Plus (monthly), Frontline Plus (monthly)"
}
```

---

## 🧪 Testing Checklist

### Cross-System Integration Tests

- [ ] **Test 1:** Adoption system can fetch pets from shelter
  - Request: `GET localhost:5001/api/pets/`
  - Expected: List of available pets

- [ ] **Test 2:** Adoption system can get pet details
  - Request: `GET localhost:5001/api/pets/1`
  - Expected: Detailed pet information

- [ ] **Test 3:** Adoption system can update pet status
  - Request: `PUT localhost:5001/api/update-status/`
  - Expected: Status changed to "adopted"

- [ ] **Test 4:** Adoption system can fetch health records
  - Request: `GET localhost:5002/api/health/1`
  - Expected: Complete health record with vaccinations

- [ ] **Test 5:** Adoption system can schedule appointments
  - Request: `POST localhost:5002/api/schedule-appointment/`
  - Expected: Appointment created successfully

- [ ] **Test 6:** Veterinary system can create health records
  - Request: `POST localhost:5002/api/health/`
  - Expected: New health record created

- [ ] **Test 7:** Veterinary system can update health records
  - Request: `POST localhost:5002/api/update-record/`
  - Expected: Health record updated

- [ ] **Test 8:** Shelter system can add new pets
  - Request: `POST localhost:5001/api/pets/`
  - Expected: New pet added

---

## 🚀 Postman Collection JSON

Import this collection into Postman:

```json
{
  "info": {
    "name": "Pet Adoption System - Complete Integration",
    "description": "API collection for testing integration between Adoption, Shelter, and Veterinary systems",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Shelter APIs",
      "item": [
        {
          "name": "Get All Pets",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{shelter_url}}/api/pets/?species=all&status=available&page=1",
              "host": ["{{shelter_url}}"],
              "path": ["api", "pets", ""],
              "query": [
                {"key": "species", "value": "all"},
                {"key": "status", "value": "available"},
                {"key": "page", "value": "1"}
              ]
            }
          }
        },
        {
          "name": "Get Pet by ID",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{shelter_url}}/api/pets/1",
              "host": ["{{shelter_url}}"],
              "path": ["api", "pets", "1"]
            }
          }
        },
        {
          "name": "Add New Pet",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"Bella\",\n  \"species\": \"dog\",\n  \"breed\": \"Golden Retriever\",\n  \"age\": 3,\n  \"gender\": \"female\",\n  \"color\": \"Golden\",\n  \"size\": \"large\"\n}"
            },
            "url": {
              "raw": "{{shelter_url}}/api/pets/",
              "host": ["{{shelter_url}}"],
              "path": ["api", "pets", ""]
            }
          }
        },
        {
          "name": "Update Pet Status",
          "request": {
            "method": "PUT",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"pet_id\": 1,\n  \"status\": \"adopted\"\n}"
            },
            "url": {
              "raw": "{{shelter_url}}/api/update-status/",
              "host": ["{{shelter_url}}"],
              "path": ["api", "update-status", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Veterinary APIs",
      "item": [
        {
          "name": "Get Health Record",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{veterinary_url}}/api/health/1",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "health", "1"]
            }
          }
        },
        {
          "name": "Create Health Record",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"pet_id\": 1,\n  \"pet_name\": \"Max\",\n  \"weight\": 65.5,\n  \"temperature\": 101.2,\n  \"vet_id\": 1\n}"
            },
            "url": {
              "raw": "{{veterinary_url}}/api/health/",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "health", ""]
            }
          }
        },
        {
          "name": "Update Health Record",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"pet_id\": 1,\n  \"weight\": 66.0,\n  \"notes\": \"Annual checkup completed\"\n}"
            },
            "url": {
              "raw": "{{veterinary_url}}/api/update-record/",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "update-record", ""]
            }
          }
        },
        {
          "name": "Schedule Appointment",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"pet_id\": 1,\n  \"pet_name\": \"Max\",\n  \"owner_name\": \"John Doe\",\n  \"owner_phone\": \"555-0123\",\n  \"owner_email\": \"john@example.com\",\n  \"vet_id\": 1,\n  \"date\": \"2025-11-20\",\n  \"time\": \"10:00\",\n  \"duration\": 30,\n  \"reason\": \"vaccination\"\n}"
            },
            "url": {
              "raw": "{{veterinary_url}}/api/schedule-appointment/",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "schedule-appointment", ""]
            }
          }
        },
        {
          "name": "Get Pet Appointments",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{veterinary_url}}/api/appointments/1",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "appointments", "1"]
            }
          }
        },
        {
          "name": "Get Veterinarians",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{veterinary_url}}/api/vets",
              "host": ["{{veterinary_url}}"],
              "path": ["api", "vets"]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "shelter_url",
      "value": "http://localhost:5001"
    },
    {
      "key": "veterinary_url",
      "value": "http://localhost:5002"
    },
    {
      "key": "adoption_url",
      "value": "http://localhost:5000"
    }
  ]
}
```

---

## 📝 Notes

- All systems must be running simultaneously for integration tests
- CORS is enabled for cross-origin requests
- Error responses follow standard HTTP status codes
- Some endpoints require authentication (implement session/token handling in Postman)
- Use Postman's environment variables for easy switching between environments

---

## 🐛 Troubleshooting

**Issue:** Connection Refused
- **Solution:** Ensure all three systems are running on correct ports

**Issue:** 404 Not Found
- **Solution:** Verify the endpoint URL and method (GET/POST/PUT)

**Issue:** Empty Response
- **Solution:** Check if database is populated with data

**Issue:** Timeout
- **Solution:** Increase request timeout in Postman (default is 5 seconds)

---

## ✅ Quick Start Commands

```bash
# Terminal 1 - Start Shelter System
python shelter_system/app.py

# Terminal 2 - Start Veterinary System
python veterinary_system/app.py

# Terminal 3 - Start Adoption System
python adoption_system/app.py

# Test Integration
curl http://localhost:5001/api/pets/
curl http://localhost:5002/api/health/1
curl http://localhost:5002/api/vets
```
