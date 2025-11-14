"""
Appointment management routes
"""
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('appointments', __name__, url_prefix='/appointments')

from veterinary_system.extensions import db
from veterinary_system.models import Appointment, Vet
from veterinary_system.utils.google_calendar import create_calendar_event, update_calendar_event, delete_calendar_event

@bp.route('/api/schedule-appointment/', methods=['POST'])
def api_schedule_appointment():
    """API endpoint to schedule appointment (called by adoption system)"""
    data = request.get_json()
    
    required_fields = ['pet_id', 'vet_id', 'date', 'reason']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Parse date
    try:
        appointment_date = datetime.fromisoformat(data['date'])
    except:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Check if vet exists
    vet = Vet.query.get(data['vet_id'])
    if not vet:
        return jsonify({'error': 'Vet not found'}), 404
    
    # Create appointment
    appointment = Appointment(
        pet_id=data['pet_id'],
        pet_name=data.get('pet_name', ''),
        owner_name=data.get('owner_name', ''),
        owner_email=data.get('owner_email', ''),
        owner_phone=data.get('owner_phone', ''),
        vet_id=data['vet_id'],
        date=appointment_date,
        duration=data.get('duration', 30),
        reason=data['reason'],
        notes=data.get('notes', ''),
        status='scheduled'
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    # Create Google Calendar event
    try:
        event_id = create_calendar_event(
            title=f"Vet Appointment - {appointment.pet_name}",
            description=f"Reason: {appointment.reason}\nOwner: {appointment.owner_name}",
            start_time=appointment.date,
            duration=appointment.duration,
            attendees=[appointment.owner_email, vet.email] if appointment.owner_email else [vet.email]
        )
        
        if event_id:
            appointment.google_calendar_event_id = event_id
            db.session.commit()
    except Exception as e:
        print(f"Failed to create calendar event: {e}")
    
    return jsonify(appointment.to_dict()), 201


@bp.route('/schedule', methods=['GET', 'POST'])
def schedule_appointment():
    """Schedule a new appointment"""
    if request.method == 'POST':
        # Get form data
        pet_id = request.form.get('pet_id')
        pet_name = request.form.get('pet_name')
        owner_name = request.form.get('owner_name')
        owner_phone = request.form.get('owner_phone')
        owner_email = request.form.get('owner_email', '')
        vet_id = request.form.get('vet_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        duration = request.form.get('duration', 30)
        reason = request.form.get('reason')
        notes = request.form.get('notes', '')
        
        # Handle "Other" reason
        if reason == 'Other':
            reason = request.form.get('reason_other', 'Other')
        
        # Combine date and time
        try:
            appointment_date = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        except:
            flash('Invalid date or time format', 'danger')
            return redirect(url_for('appointments.schedule_appointment'))
        
        # Create appointment
        appointment = Appointment(
            pet_id=int(pet_id),
            pet_name=pet_name,
            owner_name=owner_name,
            owner_phone=owner_phone,
            owner_email=owner_email,
            vet_id=int(vet_id),
            date=appointment_date,
            duration=int(duration),
            reason=reason,
            notes=notes,
            status='scheduled'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # Create Google Calendar event
        try:
            vet = Vet.query.get(vet_id)
            event_id = create_calendar_event(
                title=f"Vet Appointment - {pet_name}",
                description=f"Reason: {reason}\nOwner: {owner_name}\nPhone: {owner_phone}",
                start_time=appointment_date,
                duration=int(duration),
                attendees=[owner_email, vet.email] if owner_email and vet else []
            )
            
            if event_id:
                appointment.google_calendar_event_id = event_id
                db.session.commit()
        except Exception as e:
            print(f"Failed to create calendar event: {e}")
        
        flash(f'Appointment scheduled successfully for {pet_name}!', 'success')
        return redirect(url_for('appointments.view_appointment', appointment_id=appointment.id))
    
    # GET request - show form
    vets = Vet.query.all()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('appointments/schedule.html', vets=vets, today=today)


@bp.route('/list')
def list_appointments():
    """List all appointments"""
    status_filter = request.args.get('status', 'all')
    vet_filter = request.args.get('vet_id', 'all')
    
    query = Appointment.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if vet_filter != 'all':
        query = query.filter_by(vet_id=int(vet_filter))
    
    appointments = query.order_by(Appointment.date.desc()).all()
    vets = Vet.query.all()
    
    return render_template('appointments/list.html',
                          appointments=appointments,
                          vets=vets,
                          status_filter=status_filter,
                          vet_filter=vet_filter)


@bp.route('/<int:appointment_id>')
def view_appointment(appointment_id):
    """View appointment details"""
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('appointments/view.html', appointment=appointment)


@bp.route('/<int:appointment_id>/update', methods=['POST'])
def update_appointment(appointment_id):
    """Update appointment status"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    if status:
        appointment.status = status
    
    if notes:
        appointment.notes = notes
    
    appointment.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Update Google Calendar event
    if appointment.google_calendar_event_id:
        try:
            update_calendar_event(
                event_id=appointment.google_calendar_event_id,
                title=f"Vet Appointment - {appointment.pet_name} [{status}]",
                description=f"Reason: {appointment.reason}\nStatus: {status}\nNotes: {notes}"
            )
        except Exception as e:
            print(f"Failed to update calendar event: {e}")
    
    flash('Appointment updated successfully!', 'success')
    return redirect(url_for('appointments.view_appointment', appointment_id=appointment_id))


@bp.route('/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """Cancel appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    appointment.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Delete from Google Calendar
    if appointment.google_calendar_event_id:
        try:
            delete_calendar_event(appointment.google_calendar_event_id)
        except Exception as e:
            print(f"Failed to delete calendar event: {e}")
    
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('appointments.list_appointments'))


@bp.route('/api/appointments/<int:pet_id>', methods=['GET'])
def api_get_pet_appointments(pet_id):
    """API endpoint to get appointments for a pet"""
    appointments = Appointment.query.filter_by(pet_id=pet_id).order_by(
        Appointment.date.desc()
    ).all()
    
    return jsonify({
        'pet_id': pet_id,
        'appointments': [apt.to_dict() for apt in appointments],
        'total': len(appointments)
    })
