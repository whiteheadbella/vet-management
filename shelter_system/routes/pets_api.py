"""
API routes for Shelter System
Provides REST API for adoption system to access pet data
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('pets_api', __name__, url_prefix='/api')

from shelter_system.extensions import db
from shelter_system.models import Pet, PetImage, ShelterLog

@bp.route('/pets/', methods=['GET'])
def get_all_pets():
    """Get all pets with filtering and pagination"""
    # Get query parameters
    species = request.args.get('species', 'all')
    breed = request.args.get('breed', '')
    age = request.args.get('age', '')
    gender = request.args.get('gender', '')
    status = request.args.get('status', 'available')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Build query
    query = Pet.query
    
    # Filter by status (default to available only)
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Filter by species
    if species != 'all':
        query = query.filter_by(species=species)
    
    # Filter by breed
    if breed:
        query = query.filter(Pet.breed.ilike(f'%{breed}%'))
    
    # Filter by age
    if age:
        try:
            age_val = int(age)
            query = query.filter_by(age=age_val)
        except ValueError:
            pass
    
    # Filter by gender
    if gender:
        query = query.filter_by(gender=gender)
    
    # Search by name or description
    if search:
        query = query.filter(
            db.or_(
                Pet.name.ilike(f'%{search}%'),
                Pet.description.ilike(f'%{search}%'),
                Pet.breed.ilike(f'%{search}%')
            )
        )
    
    # Paginate
    pagination = query.order_by(Pet.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'pets': [pet.to_dict() for pet in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    })


@bp.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Get specific pet details"""
    pet = Pet.query.get_or_404(pet_id)
    return jsonify(pet.to_dict())


@bp.route('/pets/', methods=['POST'])
def add_pet():
    """Add new pet to shelter"""
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'species']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new pet
    pet = Pet(
        name=data['name'],
        species=data['species'],
        breed=data.get('breed', ''),
        age=data.get('age'),
        gender=data.get('gender'),
        color=data.get('color'),
        size=data.get('size'),
        description=data.get('description', ''),
        vaccinated=data.get('vaccinated', False),
        spayed_neutered=data.get('spayed_neutered', False),
        microchipped=data.get('microchipped', False),
        special_needs=data.get('special_needs', ''),
        good_with_kids=data.get('good_with_kids', True),
        good_with_pets=data.get('good_with_pets', True),
        energy_level=data.get('energy_level', 'medium'),
        adoption_fee=data.get('adoption_fee', 0.0),
        status='available'
    )
    
    db.session.add(pet)
    db.session.commit()
    
    # Log the action
    log = ShelterLog(
        pet_id=pet.id,
        action='added',
        description=f'Pet {pet.name} added to shelter',
        performed_by=data.get('staff_name', 'System')
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(pet.to_dict()), 201


@bp.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """Update pet information"""
    pet = Pet.query.get_or_404(pet_id)
    data = request.get_json()
    
    # Update fields
    updateable_fields = [
        'name', 'species', 'breed', 'age', 'gender', 'color', 'size',
        'description', 'vaccinated', 'spayed_neutered', 'microchipped',
        'special_needs', 'good_with_kids', 'good_with_pets', 'energy_level',
        'adoption_fee', 'status'
    ]
    
    for field in updateable_fields:
        if field in data:
            setattr(pet, field, data[field])
    
    pet.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log the action
    log = ShelterLog(
        pet_id=pet.id,
        action='updated',
        description=f'Pet {pet.name} information updated',
        performed_by=data.get('staff_name', 'System')
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(pet.to_dict())


@bp.route('/update-status/', methods=['PUT'])
def update_pet_status():
    """Update pet status (called by adoption system)"""
    data = request.get_json()
    
    pet_id = data.get('pet_id')
    status = data.get('status')
    
    if not pet_id or not status:
        return jsonify({'error': 'Missing pet_id or status'}), 400
    
    pet = Pet.query.get_or_404(pet_id)
    old_status = pet.status
    pet.status = status
    pet.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Log the action
    log = ShelterLog(
        pet_id=pet.id,
        action='status_changed',
        description=f'Pet status changed from {old_status} to {status}',
        performed_by=data.get('system', 'Adoption System')
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'pet': pet.to_dict()})


@bp.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """Delete pet from shelter"""
    pet = Pet.query.get_or_404(pet_id)
    
    db.session.delete(pet)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Pet deleted'})


@bp.route('/pets/<int:pet_id>/images', methods=['POST'])
def add_pet_image(pet_id):
    """Add image to pet"""
    pet = Pet.query.get_or_404(pet_id)
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    from werkzeug.utils import secure_filename
    from config import Config
    
    if file and Config.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        import time
        filename = f"{int(time.time())}_{filename}"
        
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Create image record
        image = PetImage(
            pet_id=pet_id,
            image_url=f'/static/uploads/{filename}',
            is_primary=len(pet.images) == 0,  # First image is primary
            caption=request.form.get('caption', '')
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify(image.to_dict()), 201
    
    return jsonify({'error': 'Invalid file type'}), 400


@bp.route('/pets/<int:pet_id>/logs', methods=['GET'])
def get_pet_logs(pet_id):
    """Get pet activity logs"""
    pet = Pet.query.get_or_404(pet_id)
    logs = ShelterLog.query.filter_by(pet_id=pet_id).order_by(
        ShelterLog.timestamp.desc()
    ).all()
    
    return jsonify({
        'pet_id': pet_id,
        'logs': [log.to_dict() for log in logs]
    })


@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get shelter statistics"""
    stats = {
        'total_pets': Pet.query.count(),
        'available': Pet.query.filter_by(status='available').count(),
        'adopted': Pet.query.filter_by(status='adopted').count(),
        'pending': Pet.query.filter_by(status='pending').count(),
        'dogs': Pet.query.filter_by(species='dog').count(),
        'cats': Pet.query.filter_by(species='cat').count(),
    }
    
    return jsonify(stats)
