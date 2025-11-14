"""
Chatbot routes for Veterinary System
Provides AI-like responses based on veterinary data
"""
from flask import Blueprint, render_template, request, jsonify
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

from veterinary_system.extensions import db
from veterinary_system.models import VetRecord, Appointment, Vet

@bp.route('/')
def chatbot_page():
    """Render chatbot interface"""
    return render_template('chatbot.html')

@bp.route('/api/chat', methods=['POST'])
def chat():
    """Process chatbot messages"""
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    if not user_message:
        return jsonify({'response': 'Please ask me something about veterinary records!'})
    
    # Process different types of queries
    response = process_query(user_message)
    
    return jsonify({'response': response})

def process_query(message):
    """Process user query and return appropriate response"""
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 I'm the Veterinary Assistant. I can help you with health records, appointments, and veterinarian information. Try asking 'How many health records?' or 'Show upcoming appointments'."
    
    # Help
    if 'help' in message or 'what can you do' in message:
        return """I can help you with:
        
📊 Statistics: "How many health records?"
📅 Appointments: "Upcoming appointments" or "Today's appointments"
🏥 Health Records: "Show recent records" or "Find record for pet [id]"
👨‍⚕️ Veterinarians: "Show vets" or "Available vets"
🔍 Search: "Find record for pet [id]"

Just ask naturally!"""
    
    # Statistics queries
    if 'how many' in message or 'total' in message or 'statistics' in message or 'stats' in message:
        total_records = VetRecord.query.count()
        total_appointments = Appointment.query.count()
        total_vets = Vet.query.count()
        
        if 'record' in message:
            return f"📊 We have **{total_records} health records** in our system."
        elif 'appointment' in message:
            upcoming = Appointment.query.filter(Appointment.appointment_date >= datetime.now()).count()
            return f"📅 We have **{total_appointments} total appointments** ({upcoming} upcoming)."
        elif 'vet' in message:
            return f"👨‍⚕️ We have **{total_vets} veterinarians** on staff."
        else:
            return f"""📊 **Veterinary System Statistics:**
            
🏥 Health Records: **{total_records}**
📅 Appointments: **{total_appointments}**
👨‍⚕️ Veterinarians: **{total_vets}**"""
    
    # Health records
    if 'health' in message or 'record' in message:
        if 'recent' in message or 'latest' in message:
            records = VetRecord.query.order_by(VetRecord.last_checkup.desc()).limit(5).all()
            
            if not records:
                return "No health records found in the system."
            
            response = "🏥 **Recent Health Records:**\n\n"
            for record in records:
                checkup_date = record.last_checkup.strftime('%Y-%m-%d') if record.last_checkup else 'No checkup'
                response += f"• Pet ID {record.pet_id} ({record.pet_name or 'Unknown'}): Last checkup {checkup_date}\n"
            
            return response
        
        else:
            total = VetRecord.query.count()
            recent = VetRecord.query.filter(
                VetRecord.last_checkup >= datetime.now() - timedelta(days=30)
            ).count() if VetRecord.query.first() and VetRecord.query.first().last_checkup else 0
            
            return f"🏥 We have **{total} total health records** ({recent} updated in the last 30 days)."
    
    # Appointments
    if 'appointment' in message:
        if 'today' in message:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            appointments = Appointment.query.filter(
                Appointment.appointment_date >= today_start,
                Appointment.appointment_date < today_end
            ).all()
            
            if not appointments:
                return "No appointments scheduled for today. All clear! ✅"
            
            response = f"📅 **Today's Appointments ({len(appointments)}):**\n\n"
            for apt in appointments:
                vet = Vet.query.get(apt.veterinarian_id)
                vet_name = f"Dr. {vet.name}" if vet else "Unknown"
                response += f"• {apt.appointment_date.strftime('%H:%M')} - Pet ID {apt.pet_id} ({apt.pet_name or 'Unknown'}) with {vet_name}\n  Reason: {apt.reason}\n"
            
            return response
        
        elif 'upcoming' in message or 'future' in message or 'scheduled' in message:
            appointments = Appointment.query.filter(
                Appointment.appointment_date >= datetime.now()
            ).order_by(Appointment.appointment_date).limit(5).all()
            
            if not appointments:
                return "No upcoming appointments scheduled."
            
            response = "📅 **Upcoming Appointments:**\n\n"
            for apt in appointments:
                vet = Vet.query.get(apt.veterinarian_id)
                vet_name = f"Dr. {vet.name}" if vet else "Unknown"
                response += f"• {apt.appointment_date.strftime('%Y-%m-%d %H:%M')} - Pet ID {apt.pet_id} ({apt.pet_name or 'Unknown'}) with {vet_name}\n"
            
            return response
        
        elif 'past' in message or 'completed' in message:
            appointments = Appointment.query.filter(
                Appointment.appointment_date < datetime.now()
            ).order_by(Appointment.appointment_date.desc()).limit(5).all()
            
            if not appointments:
                return "No past appointments found."
            
            response = "📋 **Recent Completed Appointments:**\n\n"
            for apt in appointments:
                response += f"• {apt.appointment_date.strftime('%Y-%m-%d')} - Pet ID {apt.pet_id} ({apt.pet_name or 'Unknown'}): {apt.reason}\n"
            
            return response
        
        else:
            total = Appointment.query.count()
            upcoming = Appointment.query.filter(Appointment.appointment_date >= datetime.now()).count()
            
            return f"📅 **{total} total appointments** ({upcoming} upcoming, {total-upcoming} completed)."
    
    # Veterinarians
    if 'vet' in message and 'veterinarian' not in message.lower():
        if 'available' in message or 'list' in message or 'show' in message:
            vets = Vet.query.all()
            
            if not vets:
                return "No veterinarians found in the system."
            
            response = "👨‍⚕️ **Our Veterinarians:**\n\n"
            for vet in vets:
                response += f"• **Dr. {vet.name}** ({vet.specialization or 'General Practice'})\n  📧 {vet.email} | 📞 {vet.phone}\n"
            
            return response
        
        else:
            count = Vet.query.count()
            specializations = db.session.query(Vet.specialization).distinct().all()
            spec_list = ", ".join([s[0] for s in specializations if s[0]])
            
            if spec_list:
                return f"👨‍⚕️ We have **{count} veterinarians** specializing in: {spec_list}"
            else:
                return f"👨‍⚕️ We have **{count} veterinarians** on staff."
    
    # Search by pet ID
    if 'pet' in message and any(char.isdigit() for char in message):
        import re
        pet_id_match = re.search(r'\d+', message)
        
        if pet_id_match:
            pet_id = int(pet_id_match.group())
            record = VetRecord.query.filter_by(pet_id=pet_id).first()
            
            if record:
                appointments = Appointment.query.filter_by(pet_id=pet_id).count()
                vaccinations = record.get_vaccinations() if hasattr(record, 'get_vaccinations') else []
                
                checkup_date = record.last_checkup.strftime('%Y-%m-%d') if record.last_checkup else 'No checkup recorded'
                
                return f"""🏥 **Health Record for Pet ID {pet_id}:**
                
📋 Pet Name: **{record.pet_name or 'Unknown'}**
🐾 Species: {record.species or 'Unknown'}
🔖 Breed: {record.breed or 'Unknown'}
📅 Last Checkup: {checkup_date}
⚖️ Weight: {record.weight if record.weight else 'Not recorded'} kg
💉 Vaccination Records: {len(vaccinations)} on file
📅 Appointments: {appointments}
📝 Notes: {record.notes[:150] if record.notes else 'No notes available'}"""
            else:
                return f"No health record found for Pet ID {pet_id}. The pet may not have been examined yet."
    
    # Default response
    return """I'm not sure how to answer that. Here are some things you can ask me:

💬 "How many health records?"
💬 "Show upcoming appointments"
💬 "Show available vets"
💬 "Find record for pet 1"
💬 "Today's appointments"

Or just type 'help' to see all my features!"""
