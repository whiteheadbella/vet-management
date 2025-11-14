"""
Vet management routes
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('vets', __name__, url_prefix='/vets')

from veterinary_system.extensions import db
from veterinary_system.models import Vet, Appointment

@bp.route('/')
def list_vets():
    """List all veterinarians"""
    vets = Vet.query.all()
    return render_template('vets/list.html', vets=vets)


@bp.route('/api/vets', methods=['GET'])
def api_list_vets():
    """API endpoint to list all vets"""
    vets = Vet.query.all()
    return jsonify({
        'vets': [vet.to_dict() for vet in vets],
        'total': len(vets)
    })


@bp.route('/<int:vet_id>')
def view_vet(vet_id):
    """View vet details"""
    vet = Vet.query.get_or_404(vet_id)
    appointments = Appointment.query.filter_by(vet_id=vet_id).order_by(
        Appointment.date.desc()
    ).limit(10).all()
    
    return render_template('vets/view.html', vet=vet, appointments=appointments)


@bp.route('/add', methods=['GET', 'POST'])
def add_vet():
    """Add new veterinarian"""
    if request.method == 'POST':
        vet = Vet(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            specialization=request.form.get('specialization'),
            license_number=request.form.get('license_number'),
            bio=request.form.get('bio', '')
        )
        
        db.session.add(vet)
        db.session.commit()
        
        flash(f'Veterinarian {vet.name} added successfully!', 'success')
        return redirect(url_for('vets.view_vet', vet_id=vet.id))
    
    return render_template('vets/add.html')


@bp.route('/<int:vet_id>/edit', methods=['GET', 'POST'])
def edit_vet(vet_id):
    """Edit veterinarian information"""
    vet = Vet.query.get_or_404(vet_id)
    
    if request.method == 'POST':
        vet.name = request.form.get('name', vet.name)
        vet.email = request.form.get('email', vet.email)
        vet.phone = request.form.get('phone', vet.phone)
        vet.specialization = request.form.get('specialization', vet.specialization)
        vet.license_number = request.form.get('license_number', vet.license_number)
        vet.bio = request.form.get('bio', vet.bio)
        
        db.session.commit()
        
        flash(f'Veterinarian {vet.name} updated successfully!', 'success')
        return redirect(url_for('vets.view_vet', vet_id=vet.id))
    
    return render_template('vets/edit.html', vet=vet)
