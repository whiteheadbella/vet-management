"""
Veterinary Management System - Application
Manages pet health records and appointments
"""
import sys
import os
# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import VeterinarySystemConfig

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(VeterinarySystemConfig)

# Initialize extensions
from veterinary_system.extensions import db, cors
db.init_app(app)
cors.init_app(app)

# Import models (use absolute imports)
from veterinary_system.models import Vet, VetRecord, Appointment

# Import routes (use absolute imports)
from veterinary_system.routes import health_api, appointments, vets, health_records, chatbot

# Register blueprints
app.register_blueprint(health_api.bp)
app.register_blueprint(appointments.bp)
app.register_blueprint(vets.bp)
app.register_blueprint(health_records.bp)
app.register_blueprint(chatbot.bp)

@app.route('/')
def index():
    """Veterinary system home page"""
    stats = {
        'total_vets': Vet.query.count(),
        'total_records': VetRecord.query.count(),
        'upcoming_appointments': Appointment.query.filter(
            Appointment.status == 'scheduled'
        ).count(),
        'recent_checkups': VetRecord.query.order_by(
            VetRecord.last_checkup.desc()
        ).limit(5).all()
    }
    return render_template('index.html', stats=stats)

@app.route('/dashboard')
def dashboard():
    """Veterinary dashboard"""
    appointments = Appointment.query.order_by(Appointment.date.desc()).limit(10).all()
    records = VetRecord.query.order_by(VetRecord.last_checkup.desc()).limit(10).all()
    return render_template('dashboard.html', appointments=appointments, records=records)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# CLI commands
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Veterinary database initialized!")

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    vets = [
        Vet(name='Dr. Sarah Johnson', email='sarah@vetclinic.com',
            specialization='General Practice', phone='555-0101'),
        Vet(name='Dr. Michael Chen', email='michael@vetclinic.com',
            specialization='Surgery', phone='555-0102'),
        Vet(name='Dr. Emily Rodriguez', email='emily@vetclinic.com',
            specialization='Internal Medicine', phone='555-0103'),
    ]
    
    for vet in vets:
        db.session.add(vet)
    
    db.session.commit()
    print("Sample vets added!")

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
