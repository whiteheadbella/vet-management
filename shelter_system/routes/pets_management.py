"""
Pet management routes for shelter staff
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('pets_management', __name__, url_prefix='/manage')

from shelter_system.extensions import db
from shelter_system.models import Pet, PetImage, ShelterLog

@bp.route('/pets')
def list_pets():
    """List all pets in shelter"""
    status_filter = request.args.get('status', 'all')
    species_filter = request.args.get('species', 'all')
    
    query = Pet.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if species_filter != 'all':
        query = query.filter_by(species=species_filter)
    
    pets = query.order_by(Pet.created_at.desc()).all()
    
    return render_template('manage/list_pets.html', 
                          pets=pets,
                          status_filter=status_filter,
                          species_filter=species_filter)


@bp.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    """Add new pet"""
    if request.method == 'POST':
        pet = Pet(
            name=request.form.get('name'),
            species=request.form.get('species'),
            breed=request.form.get('breed', ''),
            age=int(request.form.get('age', 0)) if request.form.get('age') else None,
            gender=request.form.get('gender'),
            color=request.form.get('color'),
            size=request.form.get('size'),
            description=request.form.get('description', ''),
            vaccinated=request.form.get('vaccinated') == 'on',
            spayed_neutered=request.form.get('spayed_neutered') == 'on',
            microchipped=request.form.get('microchipped') == 'on',
            special_needs=request.form.get('special_needs', ''),
            good_with_kids=request.form.get('good_with_kids') == 'on',
            good_with_pets=request.form.get('good_with_pets') == 'on',
            energy_level=request.form.get('energy_level', 'medium'),
            adoption_fee=float(request.form.get('adoption_fee', 0)),
            status='available'
        )
        
        db.session.add(pet)
        db.session.commit()
        
        # Log action
        log = ShelterLog(
            pet_id=pet.id,
            action='added',
            description=f'Pet {pet.name} added to shelter',
            performed_by=request.form.get('staff_name', 'Staff')
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Pet {pet.name} added successfully!', 'success')
        return redirect(url_for('pets_management.view_pet', pet_id=pet.id))
    
    return render_template('manage/add_pet.html')


@bp.route('/pets/<int:pet_id>')
def view_pet(pet_id):
    """View pet details"""
    pet = Pet.query.get_or_404(pet_id)
    logs = ShelterLog.query.filter_by(pet_id=pet_id).order_by(
        ShelterLog.timestamp.desc()
    ).all()
    
    return render_template('manage/view_pet.html', pet=pet, logs=logs)


@bp.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit pet information"""
    pet = Pet.query.get_or_404(pet_id)
    
    if request.method == 'POST':
        pet.name = request.form.get('name', pet.name)
        pet.species = request.form.get('species', pet.species)
        pet.breed = request.form.get('breed', pet.breed)
        pet.age = int(request.form.get('age', 0)) if request.form.get('age') else pet.age
        pet.gender = request.form.get('gender', pet.gender)
        pet.color = request.form.get('color', pet.color)
        pet.size = request.form.get('size', pet.size)
        pet.description = request.form.get('description', pet.description)
        pet.vaccinated = request.form.get('vaccinated') == 'on'
        pet.spayed_neutered = request.form.get('spayed_neutered') == 'on'
        pet.microchipped = request.form.get('microchipped') == 'on'
        pet.special_needs = request.form.get('special_needs', pet.special_needs)
        pet.good_with_kids = request.form.get('good_with_kids') == 'on'
        pet.good_with_pets = request.form.get('good_with_pets') == 'on'
        pet.energy_level = request.form.get('energy_level', pet.energy_level)
        pet.adoption_fee = float(request.form.get('adoption_fee', pet.adoption_fee))
        pet.status = request.form.get('status', pet.status)
        pet.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log action
        log = ShelterLog(
            pet_id=pet.id,
            action='updated',
            description=f'Pet {pet.name} information updated',
            performed_by=request.form.get('staff_name', 'Staff')
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Pet {pet.name} updated successfully!', 'success')
        return redirect(url_for('pets_management.view_pet', pet_id=pet.id))
    
    return render_template('manage/edit_pet.html', pet=pet)


@bp.route('/pets/<int:pet_id>/delete', methods=['POST'])
def delete_pet(pet_id):
    """Delete pet"""
    pet = Pet.query.get_or_404(pet_id)
    name = pet.name
    
    db.session.delete(pet)
    db.session.commit()
    
    flash(f'Pet {name} removed from system.', 'success')
    return redirect(url_for('pets_management.list_pets'))
