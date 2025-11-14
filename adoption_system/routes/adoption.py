"""
Adoption application routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('adoption', __name__, url_prefix='/adoption')

from adoption_system.extensions import db
from adoption_system.models import AdoptionApplication, AdoptedPet
from adoption_system.utils.email_service import send_email
from adoption_system.utils.api_client import get_pet_details_from_shelter

@bp.route('/apply/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def apply(pet_id):
    """Submit adoption application"""
    if current_user.role != 'adopter':
        flash('Only adopters can submit adoption applications.', 'danger')
        return redirect(url_for('pets.browse'))
    
    if request.method == 'POST':
        # Get form data
        reason = request.form.get('reason')
        experience = request.form.get('experience')
        living_situation = request.form.get('living_situation')
        has_yard = request.form.get('has_yard') == 'yes'
        other_pets = request.form.get('other_pets')
        
        # Validation
        if not all([reason, experience, living_situation]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('adoption/apply.html', pet_id=pet_id)
        
        # Check if user already applied for this pet
        existing_app = AdoptionApplication.query.filter_by(
            user_id=current_user.id,
            pet_id=pet_id,
            status='pending'
        ).first()
        
        if existing_app:
            flash('You already have a pending application for this pet.', 'warning')
            return redirect(url_for('pets.detail', pet_id=pet_id))
        
        # Get pet details from shelter system
        pet_details = get_pet_details_from_shelter(pet_id)
        pet_name = pet_details.get('name', 'Unknown') if pet_details else 'Unknown'
        
        # Create application
        application = AdoptionApplication(
            user_id=current_user.id,
            pet_id=pet_id,
            pet_name=pet_name,
            reason=reason,
            experience=experience,
            living_situation=living_situation,
            has_yard=has_yard,
            other_pets=other_pets,
            status='pending'
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Send confirmation email
        try:
            send_email(
                to=current_user.email,
                subject='Adoption Application Received',
                template='emails/application_received.html',
                name=current_user.name,
                pet_name=pet_name,
                application_id=application.id
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        flash('Your adoption application has been submitted!', 'success')
        return redirect(url_for('adoption.my_applications'))
    
    # GET request - show form
    pet_details = get_pet_details_from_shelter(pet_id)
    return render_template('adoption/apply.html', pet_id=pet_id, pet=pet_details)


@bp.route('/my-applications')
@login_required
def my_applications():
    """View user's adoption applications"""
    if current_user.role != 'adopter':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    applications = AdoptionApplication.query.filter_by(
        user_id=current_user.id
    ).order_by(AdoptionApplication.date_submitted.desc()).all()
    
    return render_template('adoption/my_applications.html', applications=applications)


@bp.route('/applications')
@login_required
def all_applications():
    """View all applications (shelter staff only)"""
    if current_user.role != 'shelter':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    status_filter = request.args.get('status', 'all')
    
    query = AdoptionApplication.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    applications = query.order_by(AdoptionApplication.date_submitted.desc()).all()
    
    return render_template('adoption/all_applications.html', 
                          applications=applications,
                          status_filter=status_filter)


@bp.route('/application/<int:app_id>')
@login_required
def view_application(app_id):
    """View detailed application"""
    application = AdoptionApplication.query.get_or_404(app_id)
    
    # Check permissions
    if current_user.role == 'adopter' and application.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get pet details
    pet_details = get_pet_details_from_shelter(application.pet_id)
    
    return render_template('adoption/view_application.html', 
                          application=application,
                          pet=pet_details)


@bp.route('/application/<int:app_id>/review', methods=['POST'])
@login_required
def review_application(app_id):
    """Approve or reject application (shelter staff only)"""
    if current_user.role != 'shelter':
        return jsonify({'error': 'Access denied'}), 403
    
    application = AdoptionApplication.query.get_or_404(app_id)
    action = request.form.get('action')
    notes = request.form.get('notes', '')
    
    if action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    
    application.status = 'approved' if action == 'approve' else 'rejected'
    application.date_reviewed = datetime.utcnow()
    application.reviewed_by = current_user.id
    application.notes = notes
    
    db.session.commit()
    
    # If approved, create adopted pet record
    if action == 'approve':
        adopted_pet = AdoptedPet(
            pet_id=application.pet_id,
            pet_name=application.pet_name,
            adopter_id=application.user_id,
            application_id=application.id,
            adoption_date=datetime.utcnow()
        )
        db.session.add(adopted_pet)
        db.session.commit()
        
        # Update pet status in shelter system
        from utils.api_client import update_pet_status_in_shelter
        update_pet_status_in_shelter(application.pet_id, 'adopted')
    
    # Send notification email
    try:
        user = application.user
        send_email(
            to=user.email,
            subject=f'Adoption Application {application.status.title()}',
            template=f'emails/application_{application.status}.html',
            name=user.name,
            pet_name=application.pet_name,
            notes=notes
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    flash(f'Application {application.status}!', 'success')
    return redirect(url_for('adoption.view_application', app_id=app_id))


@bp.route('/my-pets')
@login_required
def my_pets():
    """View adopted pets"""
    if current_user.role != 'adopter':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    adopted_pets = AdoptedPet.query.filter_by(
        adopter_id=current_user.id
    ).order_by(AdoptedPet.adoption_date.desc()).all()
    
    # Get health records for each pet
    pets_with_health = []
    for pet in adopted_pets:
        from utils.api_client import get_pet_health_from_vet
        health_info = get_pet_health_from_vet(pet.pet_id)
        pets_with_health.append({
            'pet': pet,
            'health': health_info
        })
    
    return render_template('adoption/my_pets.html', pets_with_health=pets_with_health)
