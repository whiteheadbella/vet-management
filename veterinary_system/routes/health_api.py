"""
Health record API routes for Veterinary System
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('health_api', __name__, url_prefix='/api')

from veterinary_system.extensions import db
from veterinary_system.models import VetRecord, Vet

@bp.route('/health/<int:pet_id>', methods=['GET'])
def get_health_record(pet_id):
    """Get health record for a specific pet"""
    record = VetRecord.query.filter_by(pet_id=pet_id).first()
    
    if not record:
        return jsonify({
            'pet_id': pet_id,
            'message': 'No health records found',
            'has_records': False
        }), 404
    
    return jsonify(record.to_dict())


@bp.route('/health/', methods=['POST'])
def create_health_record():
    """Create new health record"""
    data = request.get_json()
    
    pet_id = data.get('pet_id')
    if not pet_id:
        return jsonify({'error': 'pet_id is required'}), 400
    
    # Check if record already exists
    existing_record = VetRecord.query.filter_by(pet_id=pet_id).first()
    if existing_record:
        return jsonify({'error': 'Health record already exists for this pet'}), 400
    
    record = VetRecord(
        pet_id=pet_id,
        pet_name=data.get('pet_name', ''),
        weight=data.get('weight'),
        temperature=data.get('temperature'),
        notes=data.get('notes', ''),
        medications=data.get('medications', ''),
        allergies=data.get('allergies', ''),
        chronic_conditions=data.get('chronic_conditions', ''),
        dental_health=data.get('dental_health', ''),
        heartworm_status=data.get('heartworm_status', ''),
        flea_tick_prevention=data.get('flea_tick_prevention', False),
        updated_by=data.get('vet_id')
    )
    
    # Set vaccinations if provided
    if 'vaccinations' in data:
        record.set_vaccinations(data['vaccinations'])
    
    if 'last_checkup' in data:
        try:
            record.last_checkup = datetime.fromisoformat(data['last_checkup'])
        except:
            record.last_checkup = datetime.utcnow()
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify(record.to_dict()), 201


@bp.route('/update-record/', methods=['POST', 'PUT'])
def update_health_record():
    """Update health record (called by adoption system or vet)"""
    data = request.get_json()
    
    pet_id = data.get('pet_id')
    if not pet_id:
        return jsonify({'error': 'pet_id is required'}), 400
    
    record = VetRecord.query.filter_by(pet_id=pet_id).first()
    
    if not record:
        # Create new record if doesn't exist
        record = VetRecord(pet_id=pet_id)
        db.session.add(record)
    
    # Update fields
    if 'pet_name' in data:
        record.pet_name = data['pet_name']
    if 'weight' in data:
        record.weight = data['weight']
    if 'temperature' in data:
        record.temperature = data['temperature']
    if 'notes' in data:
        record.notes = data['notes']
    if 'medications' in data:
        record.medications = data['medications']
    if 'allergies' in data:
        record.allergies = data['allergies']
    if 'chronic_conditions' in data:
        record.chronic_conditions = data['chronic_conditions']
    if 'dental_health' in data:
        record.dental_health = data['dental_health']
    if 'heartworm_status' in data:
        record.heartworm_status = data['heartworm_status']
    if 'flea_tick_prevention' in data:
        record.flea_tick_prevention = data['flea_tick_prevention']
    if 'vaccinations' in data:
        record.set_vaccinations(data['vaccinations'])
    if 'updated_by' in data:
        record.updated_by = data['updated_by']
    
    if 'last_checkup' in data:
        try:
            record.last_checkup = datetime.fromisoformat(data['last_checkup'])
        except:
            record.last_checkup = datetime.utcnow()
    else:
        record.last_checkup = datetime.utcnow()
    
    record.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(record.to_dict())


@bp.route('/health/<int:pet_id>/vaccinations', methods=['POST'])
def add_vaccination(pet_id):
    """Add vaccination to pet record"""
    record = VetRecord.query.filter_by(pet_id=pet_id).first()
    
    if not record:
        return jsonify({'error': 'No health record found'}), 404
    
    data = request.get_json()
    vaccinations = record.get_vaccinations()
    
    new_vaccination = {
        'name': data.get('name'),
        'date': data.get('date', datetime.utcnow().isoformat()),
        'next_due': data.get('next_due'),
        'vet_name': data.get('vet_name', ''),
        'notes': data.get('notes', '')
    }
    
    vaccinations.append(new_vaccination)
    record.set_vaccinations(vaccinations)
    record.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(record.to_dict())


@bp.route('/records', methods=['GET'])
def get_all_records():
    """Get all health records"""
    records = VetRecord.query.order_by(VetRecord.updated_at.desc()).all()
    return jsonify({
        'records': [record.to_dict() for record in records],
        'total': len(records)
    })


@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get veterinary statistics"""
    stats = {
        'total_records': VetRecord.query.count(),
        'total_vets': Vet.query.count(),
        'recent_checkups': VetRecord.query.filter(
            VetRecord.last_checkup != None
        ).order_by(VetRecord.last_checkup.desc()).limit(5).count()
    }
    
    return jsonify(stats)
