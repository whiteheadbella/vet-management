"""
Populate shelter system with realistic pet data including breeds, characteristics, and images
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shelter_system.app import app, db
from shelter_system.models import Pet, PetImage
import requests
from datetime import datetime

# Dog breeds with detailed characteristics based on AKC data
DOG_BREEDS = [
    {
        'name': 'Max',
        'breed': 'Golden Retriever',
        'age': 2,
        'gender': 'male',
        'size': 'Large',
        'activity_level': 'High',
        'barking_level': 'Medium',
        'characteristics': 'Friendly, Intelligent, Devoted',
        'coat_type': 'Long',
        'shedding': 'Heavy',
        'trainability': 'High',
        'description': 'Friendly and energetic Golden Retriever. Great with families and children. Loves to play fetch and swim.',
        'image_keyword': 'golden-retriever'
    },
    {
        'name': 'Bella',
        'breed': 'Labrador Retriever',
        'age': 3,
        'gender': 'female',
        'size': 'Large',
        'activity_level': 'High',
        'barking_level': 'Medium',
        'characteristics': 'Outgoing, Even Tempered, Gentle',
        'coat_type': 'Short',
        'shedding': 'Heavy',
        'trainability': 'High',
        'description': 'Sweet Labrador who loves everyone. Excellent family dog, very loyal and playful.',
        'image_keyword': 'labrador'
    },
    {
        'name': 'Charlie',
        'breed': 'Beagle',
        'age': 4,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'Medium',
        'barking_level': 'High',
        'characteristics': 'Friendly, Curious, Merry',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'trainability': 'Medium',
        'description': 'Adorable Beagle with a great nose! Loves to explore and follow scents. Good with kids.',
        'image_keyword': 'beagle'
    },
    {
        'name': 'Rocky',
        'breed': 'German Shepherd',
        'age': 3,
        'gender': 'male',
        'size': 'Large',
        'activity_level': 'High',
        'barking_level': 'Medium',
        'characteristics': 'Confident, Courageous, Smart',
        'coat_type': 'Medium',
        'shedding': 'Heavy',
        'trainability': 'High',
        'description': 'Intelligent German Shepherd. Well-trained, protective, and loyal. Great for active families.',
        'image_keyword': 'german-shepherd'
    },
    {
        'name': 'Daisy',
        'breed': 'Bulldog',
        'age': 2,
        'gender': 'female',
        'size': 'Medium',
        'activity_level': 'Low',
        'barking_level': 'Low',
        'characteristics': 'Docile, Willful, Friendly',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'trainability': 'Medium',
        'description': 'Laid-back Bulldog with a sweet temperament. Perfect for apartment living.',
        'image_keyword': 'bulldog'
    },
    {
        'name': 'Cooper',
        'breed': 'Poodle',
        'age': 1,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'Medium',
        'barking_level': 'Medium',
        'characteristics': 'Intelligent, Active, Alert',
        'coat_type': 'Curly',
        'shedding': 'Low',
        'trainability': 'High',
        'description': 'Smart Standard Poodle. Hypoallergenic coat, great for allergy sufferers. Very trainable.',
        'image_keyword': 'poodle'
    },
    {
        'name': 'Duke',
        'breed': 'Rottweiler',
        'age': 4,
        'gender': 'male',
        'size': 'Large',
        'activity_level': 'Medium',
        'barking_level': 'Low',
        'characteristics': 'Loyal, Loving, Confident Guardian',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'trainability': 'High',
        'description': 'Gentle giant Rottweiler. Well-socialized and great with family. Protective but loving.',
        'image_keyword': 'rottweiler'
    },
    {
        'name': 'Luna',
        'breed': 'Siberian Husky',
        'age': 2,
        'gender': 'female',
        'size': 'Medium',
        'activity_level': 'Very High',
        'barking_level': 'High',
        'characteristics': 'Outgoing, Mischievous, Loyal',
        'coat_type': 'Thick',
        'shedding': 'Very Heavy',
        'trainability': 'Medium',
        'description': 'Beautiful Husky with striking blue eyes. Needs lots of exercise and space to run.',
        'image_keyword': 'husky'
    },
    {
        'name': 'Bailey',
        'breed': 'Dachshund',
        'age': 3,
        'gender': 'female',
        'size': 'Small',
        'activity_level': 'Medium',
        'barking_level': 'High',
        'characteristics': 'Clever, Lively, Courageous',
        'coat_type': 'Short',
        'shedding': 'Low',
        'trainability': 'Medium',
        'description': 'Spunky Dachshund with a big personality. Great watchdog, loves to cuddle.',
        'image_keyword': 'dachshund'
    },
    {
        'name': 'Zeus',
        'breed': 'Boxer',
        'age': 2,
        'gender': 'male',
        'size': 'Large',
        'activity_level': 'High',
        'barking_level': 'Medium',
        'characteristics': 'Fun-Loving, Bright, Active',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'trainability': 'High',
        'description': 'Energetic Boxer who loves to play. Great with kids and very patient.',
        'image_keyword': 'boxer'
    }
]

# Cat breeds with detailed characteristics
CAT_BREEDS = [
    {
        'name': 'Whiskers',
        'breed': 'Persian',
        'age': 2,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'Low',
        'vocalization': 'Quiet',
        'characteristics': 'Gentle, Calm, Sweet',
        'coat_type': 'Long',
        'shedding': 'Heavy',
        'grooming_needs': 'High',
        'description': 'Beautiful Persian with a luxurious coat. Very calm and loves to lounge. Perfect lap cat.',
    },
    {
        'name': 'Mittens',
        'breed': 'Maine Coon',
        'age': 3,
        'gender': 'female',
        'size': 'Large',
        'activity_level': 'Medium',
        'vocalization': 'Moderate',
        'characteristics': 'Sociable, Playful, Intelligent',
        'coat_type': 'Long',
        'shedding': 'Heavy',
        'grooming_needs': 'High',
        'description': 'Majestic Maine Coon with a friendly personality. Great with other pets and children.',
    },
    {
        'name': 'Shadow',
        'breed': 'Siamese',
        'age': 1,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'High',
        'vocalization': 'Very Vocal',
        'characteristics': 'Social, Intelligent, Vocal',
        'coat_type': 'Short',
        'shedding': 'Low',
        'grooming_needs': 'Low',
        'description': 'Talkative Siamese who loves attention. Very interactive and forms strong bonds.',
    },
    {
        'name': 'Princess',
        'breed': 'Ragdoll',
        'age': 2,
        'gender': 'female',
        'size': 'Large',
        'activity_level': 'Low',
        'vocalization': 'Quiet',
        'characteristics': 'Docile, Placid, Affectionate',
        'coat_type': 'Long',
        'shedding': 'Medium',
        'grooming_needs': 'Medium',
        'description': 'Sweet Ragdoll who goes limp when picked up. Extremely gentle and loving.',
    },
    {
        'name': 'Tiger',
        'breed': 'Bengal',
        'age': 2,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'Very High',
        'vocalization': 'Moderate',
        'characteristics': 'Confident, Alert, Energetic',
        'coat_type': 'Short',
        'shedding': 'Low',
        'grooming_needs': 'Low',
        'description': 'Exotic Bengal with leopard-like markings. Very active and loves to play.',
    },
    {
        'name': 'Misty',
        'breed': 'British Shorthair',
        'age': 4,
        'gender': 'female',
        'size': 'Medium',
        'activity_level': 'Low',
        'vocalization': 'Quiet',
        'characteristics': 'Easygoing, Dignified, Loyal',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'grooming_needs': 'Low',
        'description': 'Charming British Shorthair with a plush coat. Independent but affectionate.',
    },
    {
        'name': 'Felix',
        'breed': 'Abyssinian',
        'age': 1,
        'gender': 'male',
        'size': 'Small',
        'activity_level': 'High',
        'vocalization': 'Moderate',
        'characteristics': 'Active, Playful, Curious',
        'coat_type': 'Short',
        'shedding': 'Low',
        'grooming_needs': 'Low',
        'description': 'Energetic Abyssinian who loves to climb and explore. Very intelligent.',
    },
    {
        'name': 'Cleo',
        'breed': 'Sphynx',
        'age': 2,
        'gender': 'female',
        'size': 'Medium',
        'activity_level': 'Medium',
        'vocalization': 'Moderate',
        'characteristics': 'Extroverted, Energetic, Loyal',
        'coat_type': 'Hairless',
        'shedding': 'None',
        'grooming_needs': 'High',
        'description': 'Unique Sphynx cat. Warm to touch, very social and loves attention.',
    },
    {
        'name': 'Oliver',
        'breed': 'Scottish Fold',
        'age': 3,
        'gender': 'male',
        'size': 'Medium',
        'activity_level': 'Medium',
        'vocalization': 'Quiet',
        'characteristics': 'Sweet, Adaptable, Playful',
        'coat_type': 'Short',
        'shedding': 'Medium',
        'grooming_needs': 'Low',
        'description': 'Adorable Scottish Fold with folded ears. Very adaptable and easygoing.',
    },
    {
        'name': 'Luna',
        'breed': 'Russian Blue',
        'age': 2,
        'gender': 'female',
        'size': 'Medium',
        'activity_level': 'Medium',
        'vocalization': 'Quiet',
        'characteristics': 'Reserved, Gentle, Intelligent',
        'coat_type': 'Short',
        'shedding': 'Low',
        'grooming_needs': 'Low',
        'description': 'Elegant Russian Blue with silvery coat. Shy at first but very loyal.',
    }
]

def get_dog_image(breed_keyword):
    """Fetch dog image from Dog CEO API"""
    try:
        breed_name = breed_keyword.lower().replace('-', '/')
        url = f'https://dog.ceo/api/breed/{breed_name}/images/random'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return data['message']
    except Exception as e:
        print(f"Error fetching dog image for {breed_keyword}: {e}")
    return None

def get_cat_image():
    """Fetch cat image from Cat API"""
    try:
        url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]['url']
    except Exception as e:
        print(f"Error fetching cat image: {e}")
    return None

def populate_pets():
    """Populate database with realistic pet data"""
    print("\n=== Populating Shelter with Pet Data ===")
    
    with app.app_context():
        # Clear existing pets
        Pet.query.delete()
        PetImage.query.delete()
        db.session.commit()
        print("✓ Cleared existing pet data")
        
        # Add dogs
        print("\nAdding dogs with characteristics and images...")
        for dog_data in DOG_BREEDS:
            # Create pet
            pet = Pet(
                name=dog_data['name'],
                species='dog',
                breed=dog_data['breed'],
                age=dog_data['age'],
                gender=dog_data['gender'],
                color=dog_data.get('color', 'Mixed'),
                size=dog_data['size'],
                description=dog_data['description'],
                status='available',
                vaccinated=True,
                spayed_neutered=True,
                microchipped=True,
                adoption_fee=200.0,
                activity_level=dog_data['activity_level'],
                barking_level=dog_data.get('barking_level', 'Medium'),
                characteristics=dog_data['characteristics'],
                coat_type=dog_data['coat_type'],
                shedding=dog_data['shedding'],
                trainability=dog_data['trainability'],
                energy_level=dog_data['activity_level'].lower() if dog_data['activity_level'] != 'Very High' else 'high',
                good_with_kids=True,
                good_with_dogs=True,
                good_with_cats=True,
                good_with_pets=True
            )
            db.session.add(pet)
            db.session.flush()  # Get the pet ID
            
            # Fetch and add image
            image_url = get_dog_image(dog_data['image_keyword'])
            if image_url:
                pet_image = PetImage(
                    pet_id=pet.id,
                    image_url=image_url,
                    is_primary=True
                )
                db.session.add(pet_image)
                print(f"  ✓ Added {pet.name} - {pet.breed}")
            else:
                print(f"  ⚠ Added {pet.name} - {pet.breed} (no image)")
        
        # Add cats
        print("\nAdding cats with characteristics and images...")
        for cat_data in CAT_BREEDS:
            # Create pet
            pet = Pet(
                name=cat_data['name'],
                species='cat',
                breed=cat_data['breed'],
                age=cat_data['age'],
                gender=cat_data['gender'],
                color=cat_data.get('color', 'Mixed'),
                size=cat_data['size'],
                description=cat_data['description'],
                status='available',
                vaccinated=True,
                spayed_neutered=True,
                microchipped=True,
                adoption_fee=150.0,
                activity_level=cat_data['activity_level'],
                characteristics=cat_data['characteristics'],
                coat_type=cat_data['coat_type'],
                shedding=cat_data['shedding'],
                energy_level=cat_data['activity_level'].lower(),
                good_with_kids=True,
                good_with_dogs=True,
                good_with_cats=True,
                good_with_pets=True
            )
            db.session.add(pet)
            db.session.flush()
            
            # Fetch and add image
            image_url = get_cat_image()
            if image_url:
                pet_image = PetImage(
                    pet_id=pet.id,
                    image_url=image_url,
                    is_primary=True
                )
                db.session.add(pet_image)
                print(f"  ✓ Added {pet.name} - {pet.breed}")
            else:
                print(f"  ⚠ Added {pet.name} - {pet.breed} (no image)")
        
        db.session.commit()
        
        total_pets = Pet.query.count()
        total_dogs = Pet.query.filter_by(species='dog').count()
        total_cats = Pet.query.filter_by(species='cat').count()
        
        print(f"\n{'='*60}")
        print(f"✓ Successfully populated shelter database!")
        print(f"  Total Pets: {total_pets}")
        print(f"  Dogs: {total_dogs}")
        print(f"  Cats: {total_cats}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    populate_pets()
