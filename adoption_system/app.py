"""
Adoption System - Main Application
The central hub for pet adoption platform
"""
import sys
import os
# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from flask_mail import Mail
from config import AdoptionSystemConfig

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(AdoptionSystemConfig)

# Initialize extensions
from adoption_system.extensions import db, login_manager, mail, cors
db.init_app(app)
cors.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Import models and routes
from adoption_system.models import User, AdoptionApplication, AdoptedPet, Notification
from adoption_system.routes import auth, adoption, pets, profile, chatbot

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(adoption.bp)
app.register_blueprint(pets.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(chatbot.bp)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Main routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    if current_user.role == 'adopter':
        # Show adoption history and applications
        applications = AdoptionApplication.query.filter_by(user_id=current_user.id).order_by(AdoptionApplication.date_submitted.desc()).all()
        adopted_pets = AdoptedPet.query.filter_by(adopter_id=current_user.id).all()
        return render_template('dashboard/adopter.html', applications=applications, adopted_pets=adopted_pets)
    
    elif current_user.role == 'shelter':
        # Show shelter management dashboard
        applications = AdoptionApplication.query.order_by(AdoptionApplication.date_submitted.desc()).limit(10).all()
        return render_template('dashboard/shelter.html', applications=applications)
    
    elif current_user.role == 'vet':
        # Show veterinary dashboard
        return render_template('dashboard/vet.html')
    
    return render_template('dashboard/default.html')

# API endpoints
@app.route('/api/health/<int:pet_id>')
def get_health_records(pet_id):
    """Get health records for a pet from veterinary system"""
    from adoption_system.utils.api_client import get_pet_health_from_vet
    health_data = get_pet_health_from_vet(pet_id)
    if health_data:
        return jsonify(health_data)
    return jsonify({'error': 'No health records found'}), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# CLI commands
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from werkzeug.security import generate_password_hash
    
    # Create sample users
    users = [
        User(name='John Adopter', email='adopter@example.com', 
             password=generate_password_hash('password123'), role='adopter'),
        User(name='Shelter Manager', email='shelter@example.com', 
             password=generate_password_hash('password123'), role='shelter'),
        User(name='Dr. Veterinarian', email='vet@example.com', 
             password=generate_password_hash('password123'), role='vet'),
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print("Database seeded with sample data!")

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
