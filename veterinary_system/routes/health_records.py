"""
Health records routes
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('health_records', __name__, url_prefix='/health-records')

from veterinary_system.extensions import db
from veterinary_system.models import VetRecord

@bp.route('/')
def list_records():
    """List all health records"""
    search = request.args.get('search', '')
    species_filter = request.args.get('species', '')
    
    query = VetRecord.query
    
    if search:
        query = query.filter(
            (VetRecord.pet_name.like(f'%{search}%')) | 
            (VetRecord.pet_id == int(search) if search.isdigit() else False)
        )
    
    if species_filter:
        query = query.filter_by(species=species_filter)
    
    records = query.order_by(VetRecord.last_checkup.desc()).all()
    
    return render_template('health_records/list.html', records=records)


@bp.route('/<int:record_id>')
def view_record(record_id):
    """View detailed health record"""
    record = VetRecord.query.get_or_404(record_id)
    return render_template('health_records/view.html', record=record)


@bp.route('/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_record(record_id):
    """Edit health record"""
    record = VetRecord.query.get_or_404(record_id)
    
    if request.method == 'POST':
        # Update physical measurements
        record.weight = float(request.form.get('weight', record.weight))
        record.temperature = float(request.form.get('temperature', record.temperature))
        
        if request.form.get('heart_rate'):
            record.heart_rate = int(request.form.get('heart_rate'))
        if request.form.get('respiratory_rate'):
            record.respiratory_rate = int(request.form.get('respiratory_rate'))
        
        record.body_condition_score = request.form.get('body_condition_score', record.body_condition_score)
        record.microchip_number = request.form.get('microchip_number', record.microchip_number)
        
        # Update medical information
        record.notes = request.form.get('notes', record.notes)
        record.medications = request.form.get('medications', record.medications)
        record.allergies = request.form.get('allergies', record.allergies)
        record.chronic_conditions = request.form.get('chronic_conditions', record.chronic_conditions)
        record.medical_history = request.form.get('medical_history', record.medical_history)
        record.surgical_history = request.form.get('surgical_history', record.surgical_history)
        
        # Update preventive care
        record.heartworm_status = request.form.get('heartworm_status', record.heartworm_status)
        record.flea_tick_prevention = 'flea_tick_prevention' in request.form
        record.flea_tick_product = request.form.get('flea_tick_product', record.flea_tick_product)
        record.dental_health = request.form.get('dental_health', record.dental_health)
        record.spayed_neutered = 'spayed_neutered' in request.form
        
        # Update owner information
        record.owner_name = request.form.get('owner_name', record.owner_name)
        record.owner_phone = request.form.get('owner_phone', record.owner_phone)
        record.owner_email = request.form.get('owner_email', record.owner_email)
        
        db.session.commit()
        
        flash(f'Health record for {record.pet_name} updated successfully!', 'success')
        return redirect(url_for('health_records.view_record', record_id=record.id))
    
    return render_template('health_records/edit.html', record=record)
