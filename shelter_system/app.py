"""
Shelter Inventory System - Application
Manages pets in shelters and provides API for adoption system
"""
import sys
import os
# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import ShelterSystemConfig
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(ShelterSystemConfig)

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
from shelter_system.extensions import db, cors
db.init_app(app)
cors.init_app(app)

# Import models (use absolute imports)
from shelter_system.models import Pet, PetImage, ShelterLog

# Import routes (use absolute imports)
from shelter_system.routes import pets_api, pets_management, chatbot

# Register blueprints
app.register_blueprint(pets_api.bp)
app.register_blueprint(pets_management.bp)
app.register_blueprint(chatbot.bp)

@app.route('/')
def index():
    """Shelter system home page"""
    stats = {
        'total_pets': Pet.query.count(),
        'available': Pet.query.filter_by(status='available').count(),
        'adopted': Pet.query.filter_by(status='adopted').count(),
        'pending': Pet.query.filter_by(status='pending').count(),
        'recent_additions': Pet.query.order_by(Pet.created_at.desc()).limit(5).all(),
        'recent_logs': ShelterLog.query.order_by(ShelterLog.timestamp.desc()).limit(10).all()
    }
    return render_template('index.html', stats=stats)

@app.route('/pets')
def list_pets():
    """List all pets"""
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template('list_pets.html', pets=pets)

@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    """Add new pet to shelter"""
    if request.method == 'POST':
        # Create pet object with all fields
        pet = Pet(
            name=request.form.get('name'),
            species=request.form.get('species'),
            breed=request.form.get('breed', ''),
            age=int(request.form.get('age', 0)) if request.form.get('age') else None,
            gender=request.form.get('gender'),
            description=request.form.get('description', ''),
            status=request.form.get('status', 'available'),
            # Medical checkboxes
            vaccinated=request.form.get('vaccinated') == 'on',
            spayed_neutered=request.form.get('spayed_neutered') == 'on',
            microchipped=request.form.get('microchipped') == 'on',
            special_needs=request.form.get('special_needs', ''),
            # Behavioral traits
            good_with_kids=request.form.get('good_with_kids') == 'on',
            good_with_pets=request.form.get('good_with_pets') == 'on',
            good_with_dogs=request.form.get('good_with_dogs') == 'on',
            good_with_cats=request.form.get('good_with_cats') == 'on',
            energy_level=request.form.get('energy_level', '')
        )
        
        db.session.add(pet)
        db.session.commit()
        
        # Add primary image if provided
        image_url = request.form.get('image_url')
        if image_url:
            pet_image = PetImage(
                pet_id=pet.id,
                image_url=image_url,
                is_primary=True,
                caption=request.form.get('image_caption', '')
            )
            db.session.add(pet_image)
            db.session.commit()
        
        # Log the action in shelter_logs
        log = ShelterLog(
            pet_id=pet.id,
            action='added',
            description=f'Pet {pet.name} ({pet.species}) added to shelter inventory',
            performed_by=request.form.get('performed_by', 'Staff')
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Pet {pet.name} added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_pet.html')

@app.route('/pets/<int:pet_id>/view')
def view_pet(pet_id):
    """View pet details"""
    pet = Pet.query.get_or_404(pet_id)
    logs = ShelterLog.query.filter_by(pet_id=pet_id).order_by(ShelterLog.timestamp.desc()).all()
    return render_template('view_pet.html', pet=pet, logs=logs)

@app.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit pet information"""
    pet = Pet.query.get_or_404(pet_id)
    
    if request.method == 'POST':
        pet.name = request.form.get('name', pet.name)
        pet.species = request.form.get('species', pet.species)
        pet.breed = request.form.get('breed', pet.breed)
        pet.age = int(request.form.get('age', 0)) if request.form.get('age') else pet.age
        pet.gender = request.form.get('gender', pet.gender)
        pet.description = request.form.get('description', pet.description)
        pet.status = request.form.get('status', pet.status)
        # Medical checkboxes
        pet.vaccinated = request.form.get('vaccinated') == 'on'
        pet.spayed_neutered = request.form.get('spayed_neutered') == 'on'
        pet.microchipped = request.form.get('microchipped') == 'on'
        pet.special_needs = request.form.get('special_needs', pet.special_needs)
        # Behavioral traits
        pet.good_with_kids = request.form.get('good_with_kids') == 'on'
        pet.good_with_pets = request.form.get('good_with_pets') == 'on'
        pet.good_with_dogs = request.form.get('good_with_dogs') == 'on'
        pet.good_with_cats = request.form.get('good_with_cats') == 'on'
        pet.energy_level = request.form.get('energy_level', pet.energy_level)
        
        db.session.commit()
        
        # Log action
        log = ShelterLog(
            pet_id=pet.id,
            action='updated',
            description=f'Pet {pet.name} information updated',
            performed_by=request.form.get('performed_by', 'Staff')
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Pet {pet.name} updated successfully!', 'success')
        return redirect(url_for('view_pet', pet_id=pet.id))
    
    return render_template('edit_pet.html', pet=pet)

@app.route('/pets/<int:pet_id>/delete', methods=['POST'])
def delete_pet(pet_id):
    """Delete pet from shelter"""
    pet = Pet.query.get_or_404(pet_id)
    name = pet.name
    
    db.session.delete(pet)
    db.session.commit()
    
    flash(f'Pet {name} removed from system.', 'success')
    return redirect(url_for('list_pets'))

@app.route('/dashboard')
def dashboard():
    """Shelter management dashboard"""
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template('dashboard.html', pets=pets)

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
    print("Shelter database initialized!")

@app.cli.command()
def seed_db():
    """Seed database with sample pets"""
    sample_pets = [
        Pet(name='Max', species='dog', breed='Golden Retriever', age=2, gender='male',
            description='Friendly and energetic golden retriever', status='available'),
        Pet(name='Bella', species='cat', breed='Siamese', age=1, gender='female',
            description='Playful and affectionate siamese cat', status='available'),
        Pet(name='Charlie', species='dog', breed='Beagle', age=3, gender='male',
            description='Calm and loving beagle', status='available'),
        Pet(name='Luna', species='cat', breed='Persian', age=2, gender='female',
            description='Beautiful persian cat with fluffy coat', status='available'),
        Pet(name='Rocky', species='dog', breed='German Shepherd', age=4, gender='male',
            description='Loyal and protective german shepherd', status='available'),
    ]
    
    for pet in sample_pets:
        db.session.add(pet)
    
    db.session.commit()
    print("Sample pets added!")

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
