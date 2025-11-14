"""
Pet browsing routes with API integration
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('pets', __name__, url_prefix='/pets')

from adoption_system.utils.api_client import (
    get_all_pets_from_shelter,
    get_pet_details_from_shelter,
    get_dog_breeds,
    get_cat_breeds,
    get_random_dog_image,
    get_cat_breed_info
)
from config import AdoptionSystemConfig

@bp.route('/browse')
def browse():
    """Browse available pets"""
    # Get filter parameters
    species = request.args.get('species', 'all')
    breed = request.args.get('breed', '')
    age = request.args.get('age', '')
    gender = request.args.get('gender', '')
    page = request.args.get('page', 1, type=int)
    
    # Get pets from shelter system
    pets = get_all_pets_from_shelter(
        species=species,
        breed=breed,
        age=age,
        gender=gender,
        page=page
    )
    
    # Get breed lists for filters
    dog_breeds = get_dog_breeds()
    cat_breeds = get_cat_breeds()
    
    return render_template('pets/browse.html',
                          pets=pets,
                          dog_breeds=dog_breeds,
                          cat_breeds=cat_breeds,
                          filters={
                              'species': species,
                              'breed': breed,
                              'age': age,
                              'gender': gender
                          })


@bp.route('/<int:pet_id>')
def detail(pet_id):
    """View pet details"""
    pet = get_pet_details_from_shelter(pet_id)
    
    if not pet:
        return render_template('errors/404.html'), 404
    
    # Get additional breed information from external APIs
    breed_info = None
    if pet['species'] == 'dog':
        breed_info = {'image': get_random_dog_image(pet.get('breed', ''))}
    elif pet['species'] == 'cat':
        breed_info = get_cat_breed_info(pet.get('breed', ''))
    
    # Check if user has already applied
    has_applied = False
    if current_user.is_authenticated and current_user.role == 'adopter':
        from models import AdoptionApplication
        has_applied = AdoptionApplication.query.filter_by(
            user_id=current_user.id,
            pet_id=pet_id,
            status='pending'
        ).first() is not None
    
    return render_template('pets/detail.html',
                          pet=pet,
                          breed_info=breed_info,
                          has_applied=has_applied)


@bp.route('/search')
def search():
    """Search pets"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('pets.browse'))
    
    # Search in shelter system
    pets = get_all_pets_from_shelter(search=query)
    
    return render_template('pets/search_results.html',
                          query=query,
                          pets=pets)


@bp.route('/api/breeds/<species>')
def api_breeds(species):
    """API endpoint to get breeds for a species"""
    if species == 'dog':
        breeds = get_dog_breeds()
    elif species == 'cat':
        breeds = get_cat_breeds()
    else:
        return jsonify({'error': 'Invalid species'}), 400
    
    return jsonify({'breeds': breeds})


@bp.route('/favorites')
@login_required
def favorites():
    """View favorite pets (future feature)"""
    return render_template('pets/favorites.html')
