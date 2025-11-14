"""
Chatbot routes for Shelter System
Provides AI-like responses based on shelter data
"""
from flask import Blueprint, render_template, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

from shelter_system.extensions import db
from shelter_system.models import Pet, PetImage, ShelterLog

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
        return jsonify({'response': 'Please ask me something about our pets!'})
    
    # Process different types of queries
    response = process_query(user_message)
    
    return jsonify({'response': response})

def process_query(message):
    """Process user query and return appropriate response"""
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 I'm the Shelter Assistant. I can help you with information about our pets, statistics, and more. Try asking 'How many pets do we have?' or 'Show me available dogs'."
    
    # Help
    if 'help' in message or 'what can you do' in message:
        return """I can help you with:
        
📊 Statistics: "How many pets do we have?"
🐕 Dogs: "Show me dogs" or "How many dogs?"
🐱 Cats: "Show me cats" or "How many cats?"
✅ Available pets: "Available pets"
⏳ Pending adoptions: "Pending pets"
🏆 Adopted pets: "Adopted pets"
🔍 Search: "Find [pet name]" or "Show me [breed]"
💉 Medical info: "Vaccinated pets" or "Microchipped pets"

Just ask naturally!"""
    
    # Statistics queries
    if 'how many' in message or 'total' in message or 'statistics' in message or 'stats' in message:
        total_pets = Pet.query.count()
        available = Pet.query.filter_by(status='available').count()
        pending = Pet.query.filter_by(status='pending').count()
        adopted = Pet.query.filter_by(status='adopted').count()
        dogs = Pet.query.filter_by(species='dog').count()
        cats = Pet.query.filter_by(species='cat').count()
        
        if 'dog' in message:
            return f"🐕 We currently have **{dogs} dogs** in our shelter ({Pet.query.filter_by(species='dog', status='available').count()} available for adoption)."
        elif 'cat' in message:
            return f"🐱 We currently have **{cats} cats** in our shelter ({Pet.query.filter_by(species='cat', status='available').count()} available for adoption)."
        else:
            return f"""📊 **Shelter Statistics:**
            
🐾 Total Pets: **{total_pets}**
✅ Available: **{available}**
⏳ Pending Adoption: **{pending}**
🏠 Adopted: **{adopted}**
🐕 Dogs: **{dogs}**
🐱 Cats: **{cats}**"""
    
    # Available pets
    if 'available' in message or 'ready for adoption' in message:
        if 'dog' in message:
            pets = Pet.query.filter_by(species='dog', status='available').limit(5).all()
            species_name = "dogs"
        elif 'cat' in message:
            pets = Pet.query.filter_by(species='cat', status='available').limit(5).all()
            species_name = "cats"
        else:
            pets = Pet.query.filter_by(status='available').limit(5).all()
            species_name = "pets"
        
        if not pets:
            return f"Currently, we don't have any available {species_name}. Please check back soon!"
        
        response = f"✅ **Available {species_name.title()}:**\n\n"
        for pet in pets:
            response += f"• **{pet.name}** - {pet.breed or pet.species.title()} ({pet.age} years old, {pet.gender})\n"
        
        if len(pets) == 5:
            response += f"\n...and more! Visit /pets to see all available {species_name}."
        
        return response
    
    # Pending adoptions
    if 'pending' in message:
        pets = Pet.query.filter_by(status='pending').limit(5).all()
        
        if not pets:
            return "Great news! We have no pending adoptions right now. All our pets are either available or already in loving homes! 🏠"
        
        response = "⏳ **Pets Pending Adoption:**\n\n"
        for pet in pets:
            response += f"• **{pet.name}** - {pet.breed or pet.species.title()} (Adoption in progress)\n"
        
        return response
    
    # Adopted pets
    if 'adopted' in message or 'found home' in message:
        pets = Pet.query.filter_by(status='adopted').limit(5).all()
        count = Pet.query.filter_by(status='adopted').count()
        
        if not pets:
            return "We're working on finding homes for all our pets! No successful adoptions yet, but we're hopeful! 💕"
        
        response = f"🏠 **Recently Adopted Pets** ({count} total):\n\n"
        for pet in pets:
            response += f"• **{pet.name}** - {pet.breed or pet.species.title()} (Found forever home! 💕)\n"
        
        return response
    
    # Search by name
    if 'find' in message or 'search' in message or 'show me' in message or 'looking for' in message:
        # Extract potential pet name or breed
        words = message.split()
        search_term = None
        
        for i, word in enumerate(words):
            if word in ['find', 'search', 'show', 'looking', 'for', 'me']:
                if i + 1 < len(words):
                    search_term = words[i + 1].title()
                    break
        
        if search_term:
            # Search by name first
            pet = Pet.query.filter(Pet.name.ilike(f'%{search_term}%')).first()
            
            if pet:
                images = "with photos" if pet.images else "no photos yet"
                return f"""🔍 **Found: {pet.name}**
                
📋 **Details:**
• Species: {pet.species.title()}
• Breed: {pet.breed or 'Mixed'}
• Age: {pet.age} years old
• Gender: {pet.gender.title()}
• Status: {pet.status.title()}
• Description: {pet.description[:100]}...

💉 **Medical:**
• Vaccinated: {'✅ Yes' if pet.vaccinated else '❌ No'}
• Spayed/Neutered: {'✅ Yes' if pet.spayed_neutered else '❌ No'}
• Microchipped: {'✅ Yes' if pet.microchipped else '❌ No'}

👶 **Good with:**
• Kids: {'✅ Yes' if pet.good_with_kids else '❌ No'}
• Pets: {'✅ Yes' if pet.good_with_pets else '❌ No'}

View full details at: /pets/{pet.id}/view"""
            
            # Search by breed
            pets = Pet.query.filter(Pet.breed.ilike(f'%{search_term}%')).limit(5).all()
            if pets:
                response = f"🔍 **Found {len(pets)} {search_term}(s):**\n\n"
                for pet in pets:
                    response += f"• **{pet.name}** ({pet.age} years, {pet.status})\n"
                return response
            
            return f"Sorry, I couldn't find any pets matching '{search_term}'. Try asking 'Show me available dogs' or 'How many cats do we have?'"
        
        return "Please specify what you're looking for. Try: 'Find Max' or 'Show me Golden Retrievers'"
    
    # Medical information
    if 'vaccinated' in message or 'vaccination' in message:
        vaccinated_count = Pet.query.filter_by(vaccinated=True).count()
        total = Pet.query.count()
        return f"💉 **{vaccinated_count} out of {total} pets** are fully vaccinated ({int(vaccinated_count/total*100)}%)! We take pet health seriously! 🏥"
    
    if 'microchip' in message:
        microchipped_count = Pet.query.filter_by(microchipped=True).count()
        total = Pet.query.count()
        return f"📍 **{microchipped_count} out of {total} pets** are microchipped ({int(microchipped_count/total*100)}%)! This helps reunite lost pets with their families! 🔍"
    
    if 'spay' in message or 'neuter' in message:
        fixed_count = Pet.query.filter_by(spayed_neutered=True).count()
        total = Pet.query.count()
        return f"✂️ **{fixed_count} out of {total} pets** are spayed/neutered ({int(fixed_count/total*100)}%)! This is important for pet health and population control! 🏥"
    
    # Activity logs
    if 'recent' in message or 'latest' in message or 'activity' in message:
        logs = ShelterLog.query.order_by(ShelterLog.timestamp.desc()).limit(5).all()
        
        if not logs:
            return "No recent activity to show."
        
        response = "📝 **Recent Activity:**\n\n"
        for log in logs:
            pet = Pet.query.get(log.pet_id)
            pet_name = pet.name if pet else "Unknown"
            response += f"• {log.action.title()}: {pet_name} - {log.description}\n"
        
        return response
    
    # Good with kids/pets
    if 'kid' in message or 'children' in message:
        count = Pet.query.filter_by(good_with_kids=True, status='available').count()
        pets = Pet.query.filter_by(good_with_kids=True, status='available').limit(3).all()
        
        if not pets:
            return "We're currently updating our pet profiles. Please check back soon!"
        
        response = f"👶 **{count} available pets are great with kids!**\n\n"
        for pet in pets:
            response += f"• **{pet.name}** - {pet.breed or pet.species.title()}\n"
        
        return response
    
    # Default response
    return """I'm not sure how to answer that. Here are some things you can ask me:

💬 "How many pets do we have?"
💬 "Show me available dogs"
💬 "Find Max" (search by name)
💬 "Pets good with kids"
💬 "Recent activity"

Or just type 'help' to see all my features!"""
