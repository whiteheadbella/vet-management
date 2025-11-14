"""
Database models for Shelter Inventory System
"""
from datetime import datetime
from shelter_system.extensions import db

class Pet(db.Model):
    """Pet model for shelter inventory"""
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(20), nullable=False)  # dog, cat
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)  # Age in years
    gender = db.Column(db.String(10))  # male, female
    color = db.Column(db.String(50))
    size = db.Column(db.String(20))  # small, medium, large
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='available')  # available, adopted, pending
    
    # Medical info
    vaccinated = db.Column(db.Boolean, default=False)
    spayed_neutered = db.Column(db.Boolean, default=False)
    microchipped = db.Column(db.Boolean, default=False)
    special_needs = db.Column(db.Text)
    
    # Behavioral traits
    good_with_kids = db.Column(db.Boolean, default=True)
    good_with_pets = db.Column(db.Boolean, default=True)
    good_with_dogs = db.Column(db.Boolean, default=True)
    good_with_cats = db.Column(db.Boolean, default=True)
    energy_level = db.Column(db.String(20))  # low, medium, high
    
    # Dog-specific characteristics (from AKC)
    activity_level = db.Column(db.String(20))  # Low, Medium, High, Very High
    barking_level = db.Column(db.String(20))  # Low, Medium, High
    characteristics = db.Column(db.String(200))  # e.g., "Friendly, Intelligent, Devoted"
    coat_type = db.Column(db.String(50))  # Short, Medium, Long, Curly, Thick, Hairless
    shedding = db.Column(db.String(20))  # Low, Medium, Heavy, Very Heavy, None
    trainability = db.Column(db.String(20))  # Low, Medium, High
    
    # Shelter info
    intake_date = db.Column(db.DateTime, default=datetime.utcnow)
    adoption_fee = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('PetImage', backref='pet', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('ShelterLog', backref='pet', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert pet to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender,
            'color': self.color,
            'size': self.size,
            'description': self.description,
            'status': self.status,
            'vaccinated': self.vaccinated,
            'spayed_neutered': self.spayed_neutered,
            'microchipped': self.microchipped,
            'special_needs': self.special_needs,
            'good_with_kids': self.good_with_kids,
            'good_with_pets': self.good_with_pets,
            'good_with_dogs': self.good_with_dogs,
            'good_with_cats': self.good_with_cats,
            'energy_level': self.energy_level,
            'activity_level': self.activity_level,
            'barking_level': self.barking_level,
            'characteristics': self.characteristics,
            'coat_type': self.coat_type,
            'shedding': self.shedding,
            'trainability': self.trainability,
            'intake_date': self.intake_date.isoformat() if self.intake_date else None,
            'adoption_fee': self.adoption_fee,
            'images': [img.to_dict() for img in self.images],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Pet {self.name} - {self.species}>'


class PetImage(db.Model):
    """Pet images"""
    __tablename__ = 'pet_images'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    caption = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert image to dictionary"""
        return {
            'id': self.id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'caption': self.caption,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    def __repr__(self):
        return f'<PetImage {self.id} for Pet {self.pet_id}>'


class ShelterLog(db.Model):
    """Log of pet status changes and activities"""
    __tablename__ = 'shelter_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # added, updated, adopted, returned
    description = db.Column(db.Text)
    performed_by = db.Column(db.String(100))  # Staff member name
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert log to dictionary"""
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'action': self.action,
            'description': self.description,
            'performed_by': self.performed_by,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<ShelterLog {self.action} - Pet {self.pet_id}>'
