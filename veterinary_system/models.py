"""
Database models for Veterinary Management System
"""
from datetime import datetime
import json
from veterinary_system.extensions import db

class Vet(db.Model):
    """Veterinarian model"""
    __tablename__ = 'vets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='vet', lazy=True)
    
    def to_dict(self):
        """Convert vet to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'bio': self.bio
        }
    
    def __repr__(self):
        return f'<Vet {self.name}>'


class VetRecord(db.Model):
    """Pet health record"""
    __tablename__ = 'vet_records'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False, index=True)  # Reference to pet from shelter
    pet_name = db.Column(db.String(100))
    species = db.Column(db.String(20))  # dog, cat
    breed = db.Column(db.String(100))
    
    # Owner information
    owner_name = db.Column(db.String(100))
    owner_phone = db.Column(db.String(20))
    owner_email = db.Column(db.String(120))
    
    # Basic health information
    last_checkup = db.Column(db.DateTime)
    weight = db.Column(db.Float)  # in kg or lbs
    temperature = db.Column(db.Float)  # in celsius or fahrenheit
    heart_rate = db.Column(db.Integer)  # beats per minute
    respiratory_rate = db.Column(db.Integer)  # breaths per minute
    
    # Physical examination
    body_condition_score = db.Column(db.String(20))  # 1-9 scale
    microchip_number = db.Column(db.String(50))
    spayed_neutered = db.Column(db.Boolean, default=False)
    spay_neuter_date = db.Column(db.DateTime)
    
    # Vaccinations stored as JSON (includes date, type, manufacturer, lot number, next due date)
    vaccinations = db.Column(db.Text)  # JSON string
    
    # Deworming history stored as JSON
    deworming_records = db.Column(db.Text)  # JSON string
    
    # Medical notes and history
    notes = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    surgical_history = db.Column(db.Text)
    medications = db.Column(db.Text)  # Current medications
    allergies = db.Column(db.Text)
    chronic_conditions = db.Column(db.Text)
    
    # Preventive care
    dental_health = db.Column(db.String(50))  # excellent, good, fair, poor
    dental_cleaning_date = db.Column(db.DateTime)
    heartworm_status = db.Column(db.String(50))  # negative, positive
    heartworm_test_date = db.Column(db.DateTime)
    flea_tick_prevention = db.Column(db.Boolean, default=False)
    flea_tick_product = db.Column(db.String(100))
    flea_tick_last_applied = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('vets.id'))
    
    def get_vaccinations(self):
        """Get vaccinations as list"""
        if self.vaccinations:
            try:
                return json.loads(self.vaccinations)
            except:
                return []
        return []
    
    def set_vaccinations(self, vaccinations_list):
        """Set vaccinations from list"""
        self.vaccinations = json.dumps(vaccinations_list)
    
    def get_deworming_records(self):
        """Get deworming records as list"""
        if self.deworming_records:
            try:
                return json.loads(self.deworming_records)
            except:
                return []
        return []
    
    def set_deworming_records(self, deworming_list):
        """Set deworming records from list"""
        self.deworming_records = json.dumps(deworming_list)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'pet_name': self.pet_name,
            'species': self.species,
            'breed': self.breed,
            'owner_name': self.owner_name,
            'owner_phone': self.owner_phone,
            'owner_email': self.owner_email,
            'last_checkup': self.last_checkup.isoformat() if self.last_checkup else None,
            'weight': self.weight,
            'temperature': self.temperature,
            'heart_rate': self.heart_rate,
            'respiratory_rate': self.respiratory_rate,
            'body_condition_score': self.body_condition_score,
            'microchip_number': self.microchip_number,
            'spayed_neutered': self.spayed_neutered,
            'spay_neuter_date': self.spay_neuter_date.isoformat() if self.spay_neuter_date else None,
            'vaccinations': self.get_vaccinations(),
            'deworming_records': self.get_deworming_records(),
            'notes': self.notes,
            'medical_history': self.medical_history,
            'surgical_history': self.surgical_history,
            'medications': self.medications,
            'allergies': self.allergies,
            'chronic_conditions': self.chronic_conditions,
            'dental_health': self.dental_health,
            'dental_cleaning_date': self.dental_cleaning_date.isoformat() if self.dental_cleaning_date else None,
            'heartworm_status': self.heartworm_status,
            'heartworm_test_date': self.heartworm_test_date.isoformat() if self.heartworm_test_date else None,
            'flea_tick_prevention': self.flea_tick_prevention,
            'flea_tick_product': self.flea_tick_product,
            'flea_tick_last_applied': self.flea_tick_last_applied.isoformat() if self.flea_tick_last_applied else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<VetRecord Pet {self.pet_id}>'


class Appointment(db.Model):
    """Vet appointment"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False, index=True)
    pet_name = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    owner_email = db.Column(db.String(120))
    owner_phone = db.Column(db.String(20))
    
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'), nullable=False)
    
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=30)  # Duration in minutes
    reason = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    
    # Google Calendar integration
    google_calendar_event_id = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'pet_name': self.pet_name,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'owner_phone': self.owner_phone,
            'vet_id': self.vet_id,
            'vet_name': self.vet.name if self.vet else None,
            'date': self.date.isoformat() if self.date else None,
            'duration': self.duration,
            'reason': self.reason,
            'notes': self.notes,
            'status': self.status,
            'google_calendar_event_id': self.google_calendar_event_id
        }
    
    def __repr__(self):
        return f'<Appointment {self.id} - Pet {self.pet_id}>'
