"""
Database models for Adoption System
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from adoption_system.extensions import db

class User(UserMixin, db.Model):
    """User model for adopters, shelter staff, and vets"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # adopter, shelter, vet
    gender = db.Column(db.String(10))  # male, female, other
    job = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    adoption_applications = db.relationship('AdoptionApplication', 
                                          foreign_keys='AdoptionApplication.user_id',
                                          backref='user', lazy=True)
    adopted_pets = db.relationship('AdoptedPet', backref='adopter', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'


class AdoptionApplication(db.Model):
    """Adoption application submitted by users"""
    __tablename__ = 'adoption_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, nullable=False)  # Reference to pet in shelter system
    pet_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    reason = db.Column(db.Text)  # Why they want to adopt
    experience = db.Column(db.Text)  # Previous pet experience
    living_situation = db.Column(db.String(100))  # House/Apartment
    has_yard = db.Column(db.Boolean, default=False)
    other_pets = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    date_reviewed = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AdoptionApplication {self.id} - Pet {self.pet_id}>'


class AdoptedPet(db.Model):
    """Record of successfully adopted pets"""
    __tablename__ = 'adopted_pets'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False)  # Reference to pet in shelter system
    pet_name = db.Column(db.String(100))
    adopter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('adoption_applications.id'))
    adoption_date = db.Column(db.DateTime, default=datetime.utcnow)
    adoption_fee = db.Column(db.Float, default=0.0)
    microchip_number = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AdoptedPet {self.pet_name} by User {self.adopter_id}>'


class Notification(db.Model):
    """Email/notification log"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50))  # email, sms, in-app
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='sent')  # sent, failed, read
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.notification_type}>'
