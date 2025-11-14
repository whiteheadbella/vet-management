"""
Chatbot routes for Adoption System
Provides AI-like responses based on adoption data and integrates with other systems
"""
from flask import Blueprint, render_template, request, jsonify
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

SHELTER_API = "http://localhost:5001/api"
VET_API = "http://localhost:5002/api"

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
        return jsonify({'response': 'Please ask me something about pet adoption!'})
    
    # Process different types of queries
    response = process_query(user_message)
    
    return jsonify({'response': response})

def process_query(message):
    """Process user query and return appropriate response"""
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 I'm the Adoption Assistant. I can help you find pets available for adoption, check their health status, and guide you through the adoption process. Try asking 'Show me available pets' or 'How does adoption work?'."
    
    # Help
    if 'help' in message or 'what can you do' in message:
        return "I can help you with:\n\n" + \
               "🐾 Available Pets: \"Show me available pets\" or \"Dogs for adoption\"\n" + \
               "🔍 Search: \"Find [pet name]\" or \"Show me puppies\"\n" + \
               "🏥 Health Info: \"Check health status for pet [id]\"\n" + \
               "❤️ Adoption Process: \"How to adopt?\" or \"Adoption steps\"\n" + \
               "📊 Statistics: \"How many pets available?\"\n" + \
               "👶 Family-Friendly: \"Pets good with kids\"\n\n" + \
               "I can also integrate information from our Shelter and Veterinary systems!"
    
    # Adoption process
    if 'adopt' in message and ('how' in message or 'process' in message or 'steps' in message or 'work' in message):
        return """❤️ **Adoption Process:**

**Step 1: Browse Pets** 🔍
Visit our shelter system to see all available pets

**Step 2: Meet Your Match** 🐾
Find a pet that fits your lifestyle and family

**Step 3: Health Check** 🏥
Review the pet's health records and vaccination status

**Step 4: Submit Application** 📝
Fill out our adoption application form

**Step 5: Home Visit** 🏠
Schedule a home visit to ensure good environment

**Step 6: Finalize Adoption** ✅
Complete paperwork and take your new friend home!

**Step 7: Follow-up Care** 💕
Schedule first vet appointment within 2 weeks

Would you like to see available pets?"""
    
    # Available pets from Shelter System
    if 'available' in message or 'adoption' in message or 'find pet' in message:
        try:
            response = requests.get(f"{SHELTER_API}/pets/", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                available_pets = [p for p in data.get('pets', []) if p['status'] == 'available']
                
                if 'dog' in message:
                    available_pets = [p for p in available_pets if p['species'] == 'dog']
                    species_name = "dogs"
                elif 'cat' in message:
                    available_pets = [p for p in available_pets if p['species'] == 'cat']
                    species_name = "cats"
                elif 'puppy' in message or 'puppies' in message:
                    available_pets = [p for p in available_pets if p['species'] == 'dog' and p['age'] <= 1]
                    species_name = "puppies"
                elif 'kitten' in message:
                    available_pets = [p for p in available_pets if p['species'] == 'cat' and p['age'] <= 1]
                    species_name = "kittens"
                else:
                    species_name = "pets"
                
                if not available_pets:
                    return f"Sorry, we don't have any {species_name} available right now. Check back soon!"
                
                result = f"🐾 **Available {species_name.title()} ({len(available_pets)}):**\n\n"
                
                for pet in available_pets[:5]:
                    result += f"• **{pet['name']}** (ID: {pet['id']})\n"
                    result += f"  {pet['breed'] or pet['species'].title()}, {pet['age']} years, {pet['gender']}\n"
                    if pet.get('good_with_kids'):
                        result += f"  👶 Great with kids!\n"
                    result += "\n"
                
                if len(available_pets) > 5:
                    result += f"...and {len(available_pets) - 5} more!\n\n"
                
                result += "Ask me about specific pets or their health status!"
                return result
            else:
                return "I'm having trouble connecting to the Shelter System. Please try again later."
        
        except Exception as e:
            return "Unable to fetch pets from Shelter System right now. Please try again."
    
    # Statistics
    if 'how many' in message or 'statistics' in message or 'stats' in message:
        try:
            response = requests.get(f"{SHELTER_API}/pets/statistics", timeout=5)
            
            if response.status_code == 200:
                stats = response.json()
                
                return f"""📊 **Adoption Statistics:**
                
🐾 Total Pets: **{stats['total_pets']}**
✅ Available for Adoption: **{stats['available']}**
⏳ Adoption Pending: **{stats['pending']}**
🏠 Successfully Adopted: **{stats['adopted']}**

🐕 Dogs: **{stats['dogs']}**
🐱 Cats: **{stats['cats']}**

Ready to find your perfect match? Ask me to show available pets!"""
            else:
                return "Unable to fetch statistics right now."
        
        except Exception as e:
            return "Statistics temporarily unavailable. Please try again."
    
    # Health check integration
    if 'health' in message:
        import re
        pet_id_match = re.search(r'\d+', message)
        
        if pet_id_match:
            pet_id = int(pet_id_match.group())
            
            try:
                # Get pet info from shelter
                shelter_response = requests.get(f"{SHELTER_API}/pets/{pet_id}", timeout=5)
                # Get health info from vet
                vet_response = requests.get(f"{VET_API}/health/{pet_id}", timeout=5)
                
                if shelter_response.status_code == 200 and vet_response.status_code == 200:
                    pet = shelter_response.json()
                    health = vet_response.json()
                    
                    return f"""🏥 **Health Status for {pet['name']}:**
                    
📋 **Basic Info:**
• Species: {pet['species'].title()}
• Breed: {pet.get('breed', 'Mixed')}
• Age: {pet['age']} years
• Gender: {pet['gender'].title()}

💉 **Medical Status:**
• Vaccinated: {'✅ Yes' if pet.get('vaccinated') else '❌ No'}
• Spayed/Neutered: {'✅ Yes' if pet.get('spayed_neutered') else '❌ No'}
• Microchipped: {'✅ Yes' if pet.get('microchipped') else '❌ No'}

🏥 **Veterinary Records:**
• Health Status: **{health.get('health_status', 'N/A').title()}**
• Last Checkup: {health.get('last_checkup', 'Not recorded')}
• Weight: {health.get('weight', 'N/A')} kg

{pet['name']} is ready for adoption! Would you like to know more?"""
                else:
                    return f"Unable to find complete information for Pet ID {pet_id}."
            
            except Exception as e:
                return "Unable to fetch health information right now. Please try again."
        else:
            return "Please specify a pet ID. Example: 'Check health status for pet 1'"
    
    # Kid-friendly pets
    if 'kid' in message or 'children' in message or 'family' in message:
        try:
            response = requests.get(f"{SHELTER_API}/pets/", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                kid_friendly = [p for p in data.get('pets', []) 
                               if p['status'] == 'available' and p.get('good_with_kids')]
                
                if not kid_friendly:
                    return "We're updating our pet profiles. Please check back soon!"
                
                result = f"👶 **Family-Friendly Pets ({len(kid_friendly)}):**\n\n"
                
                for pet in kid_friendly[:5]:
                    result += f"• **{pet['name']}** - {pet['breed'] or pet['species'].title()} ({pet['age']} years)\n"
                    result += f"  Perfect for families with children!\n\n"
                
                if len(kid_friendly) > 5:
                    result += f"...and {len(kid_friendly) - 5} more!\n\n"
                
                return result + "These pets are great with kids!"
            else:
                return "Unable to fetch pet information right now."
        
        except Exception as e:
            return "Unable to search for family-friendly pets. Please try again."
    
    # Search by name
    if 'find' in message or 'search' in message or 'show me' in message:
        words = message.split()
        search_term = None
        
        for i, word in enumerate(words):
            if word in ['find', 'search', 'show', 'me']:
                if i + 1 < len(words) and words[i + 1] not in ['pet', 'pets', 'dog', 'cat']:
                    search_term = words[i + 1].title()
                    break
        
        if search_term:
            try:
                response = requests.get(f"{SHELTER_API}/pets/", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    found = [p for p in data.get('pets', []) 
                            if search_term.lower() in p['name'].lower() or 
                               (p.get('breed') and search_term.lower() in p['breed'].lower())]
                    
                    if found:
                        pet = found[0]
                        return f"""🔍 **Found: {pet['name']}!**
                        
📋 **Details:**
• ID: {pet['id']}
• Species: {pet['species'].title()}
• Breed: {pet.get('breed', 'Mixed')}
• Age: {pet['age']} years
• Gender: {pet['gender'].title()}
• Status: {pet['status'].title()}

💝 **Perfect For:**
• Kids: {'✅ Yes' if pet.get('good_with_kids') else '❌ No'}
• Other Pets: {'✅ Yes' if pet.get('good_with_pets') else '❌ No'}

Want to know more? Ask me to check {pet['name']}'s health status!"""
                    else:
                        return f"Sorry, I couldn't find any pets matching '{search_term}'. Try asking 'Show me available dogs' or 'Available cats'."
            
            except Exception as e:
                return "Unable to search right now. Please try again."
    
    # Default response
    return """I'm not sure how to answer that. Here are some things you can ask me:

💬 "Show me available pets"
💬 "Dogs for adoption"
💬 "How to adopt?"
💬 "Check health status for pet 1"
💬 "Pets good with kids"
💬 "Find Max"

Or just type 'help' to see all my features!"""
