"""
Populate veterinary system with comprehensive health records including vaccinations
Based on standard puppy/kitten health record format
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from veterinary_system.app import app, db
from veterinary_system.models import Vet, VetRecord, Appointment
from shelter_system.app import app as shelter_app
from shelter_system.models import Pet
from datetime import datetime, timedelta
import random
import json

# Standard dog vaccinations based on puppy health records
DOG_VACCINATIONS = {
    'core': [
        {
            'name': 'DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza)',
            'short_name': 'DHPP',
            'series': True,
            'doses': 3,
            'interval_weeks': 3,
            'booster_years': 3
        },
        {
            'name': 'Rabies',
            'short_name': 'Rabies',
            'series': False,
            'doses': 1,
            'booster_years': 1
        },
    ],
    'non_core': [
        {
            'name': 'Bordetella (Kennel Cough)',
            'short_name': 'Bordetella',
            'series': False,
            'doses': 1,
            'booster_months': 6
        },
        {
            'name': 'Lyme Disease',
            'short_name': 'Lyme',
            'series': True,
            'doses': 2,
            'interval_weeks': 3,
            'booster_years': 1
        },
        {
            'name': 'Leptospirosis',
            'short_name': 'Lepto',
            'series': True,
            'doses': 2,
            'interval_weeks': 3,
            'booster_years': 1
        },
        {
            'name': 'Canine Influenza',
            'short_name': 'CIV',
            'series': True,
            'doses': 2,
            'interval_weeks': 3,
            'booster_years': 1
        }
    ]
}

# Standard cat vaccinations
CAT_VACCINATIONS = {
    'core': [
        {
            'name': 'FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)',
            'short_name': 'FVRCP',
            'series': True,
            'doses': 3,
            'interval_weeks': 3,
            'booster_years': 3
        },
        {
            'name': 'Rabies',
            'short_name': 'Rabies',
            'series': False,
            'doses': 1,
            'booster_years': 1
        },
    ],
    'non_core': [
        {
            'name': 'FeLV (Feline Leukemia)',
            'short_name': 'FeLV',
            'series': True,
            'doses': 2,
            'interval_weeks': 3,
            'booster_years': 1
        },
        {
            'name': 'FIV (Feline Immunodeficiency Virus)',
            'short_name': 'FIV',
            'series': True,
            'doses': 3,
            'interval_weeks': 3,
            'booster_years': 1
        }
    ]
}

# Vaccine manufacturers
MANUFACTURERS = [
    'Merck Animal Health',
    'Zoetis',
    'Boehringer Ingelheim',
    'Elanco',
    'Virbac'
]

# Deworming products
DEWORMING_PRODUCTS = [
    'Pyrantel Pamoate',
    'Fenbendazole (Panacur)',
    'Praziquantel',
    'Drontal Plus',
    'Interceptor Plus'
]

def generate_lot_number():
    """Generate a realistic vaccine lot number"""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    numbers = ''.join(random.choices('0123456789', k=6))
    return f"{letters}{numbers}"

def generate_vaccination_history(species, age_months):
    """Generate realistic vaccination history based on age"""
    vaccinations = []
    base_date = datetime.now() - timedelta(days=age_months * 30)
    
    if species == 'dog':
        vax_list = DOG_VACCINATIONS
    else:
        vax_list = CAT_VACCINATIONS
    
    # Core vaccinations (always given)
    for vax in vax_list['core']:
        if vax['series']:
            # Multi-dose series
            for dose in range(1, vax['doses'] + 1):
                dose_date = base_date + timedelta(weeks=vax['interval_weeks'] * (dose - 1))
                if dose_date <= datetime.now():
                    vaccinations.append({
                        'vaccine_name': vax['name'],
                        'short_name': vax['short_name'],
                        'date_given': dose_date.strftime('%Y-%m-%d'),
                        'dose_number': f"{dose}/{vax['doses']}",
                        'manufacturer': random.choice(MANUFACTURERS),
                        'lot_number': generate_lot_number(),
                        'administered_by': 'Dr. Sarah Johnson',
                        'next_due': (dose_date + timedelta(days=365 * vax.get('booster_years', 1))).strftime('%Y-%m-%d') if dose == vax['doses'] else None,
                        'site': random.choice(['Left shoulder', 'Right shoulder', 'Left rear leg', 'Right rear leg']),
                        'route': 'Subcutaneous'
                    })
        else:
            # Single dose
            dose_date = base_date + timedelta(weeks=16)  # Typically given at 16 weeks
            if dose_date <= datetime.now():
                vaccinations.append({
                    'vaccine_name': vax['name'],
                    'short_name': vax['short_name'],
                    'date_given': dose_date.strftime('%Y-%m-%d'),
                    'dose_number': '1/1',
                    'manufacturer': random.choice(MANUFACTURERS),
                    'lot_number': generate_lot_number(),
                    'administered_by': 'Dr. Sarah Johnson',
                    'next_due': (dose_date + timedelta(days=365 * vax.get('booster_years', 1))).strftime('%Y-%m-%d'),
                    'site': random.choice(['Left shoulder', 'Right shoulder']),
                    'route': 'Intramuscular'
                })
    
    # Non-core vaccinations (50% chance)
    for vax in vax_list['non_core']:
        if random.random() > 0.5:
            if vax['series']:
                for dose in range(1, vax['doses'] + 1):
                    dose_date = base_date + timedelta(weeks=12 + vax['interval_weeks'] * (dose - 1))
                    if dose_date <= datetime.now():
                        vaccinations.append({
                            'vaccine_name': vax['name'],
                            'short_name': vax['short_name'],
                            'date_given': dose_date.strftime('%Y-%m-%d'),
                            'dose_number': f"{dose}/{vax['doses']}",
                            'manufacturer': random.choice(MANUFACTURERS),
                            'lot_number': generate_lot_number(),
                            'administered_by': 'Dr. Michael Chen',
                            'next_due': (dose_date + timedelta(days=365 * vax.get('booster_years', 1))).strftime('%Y-%m-%d') if dose == vax['doses'] else None,
                            'site': random.choice(['Left shoulder', 'Right shoulder', 'Left rear leg']),
                            'route': 'Subcutaneous'
                        })
    
    return vaccinations

def generate_deworming_history(age_months):
    """Generate deworming history"""
    deworming = []
    base_date = datetime.now() - timedelta(days=age_months * 30)
    
    # Puppies/kittens typically dewormed at 2, 4, 6, 8 weeks, then every 3 months
    deworming_ages = [2, 4, 6, 8, 12, 16, 20, 24]
    
    for weeks in deworming_ages:
        if weeks / 4 <= age_months:
            deworming_date = base_date + timedelta(weeks=weeks)
            if deworming_date <= datetime.now():
                deworming.append({
                    'date': deworming_date.strftime('%Y-%m-%d'),
                    'product': random.choice(DEWORMING_PRODUCTS),
                    'weight_at_treatment': round(random.uniform(2.0, 30.0), 1),
                    'administered_by': random.choice(['Dr. Sarah Johnson', 'Dr. Michael Chen', 'Dr. Emily Rodriguez']),
                    'notes': random.choice([
                        'No adverse reactions',
                        'Well tolerated',
                        'Routine deworming',
                        'Preventive treatment'
                    ])
                })
    
    return deworming

def populate_health_records():
    """Populate veterinary system with comprehensive health records"""
    print("\n=== Populating Veterinary Health Records ===")
    
    with app.app_context():
        # Clear existing records
        VetRecord.query.delete()
        Appointment.query.delete()
        Vet.query.delete()
        db.session.commit()
        print("✓ Cleared existing veterinary data")
        
        # Create veterinarians
        vets = [
            Vet(
                name='Dr. Sarah Johnson',
                email='sarah.johnson@vetclinic.com',
                phone='555-0101',
                specialization='General Practice',
                license_number='VET-2018-1234',
                bio='15 years of experience in small animal medicine'
            ),
            Vet(
                name='Dr. Michael Chen',
                email='michael.chen@vetclinic.com',
                phone='555-0102',
                specialization='Surgery',
                license_number='VET-2015-5678',
                bio='Specialist in orthopedic and soft tissue surgery'
            ),
            Vet(
                name='Dr. Emily Rodriguez',
                email='emily.rodriguez@vetclinic.com',
                phone='555-0103',
                specialization='Internal Medicine',
                license_number='VET-2020-9012',
                bio='Board certified in veterinary internal medicine'
            )
        ]
        
        for vet in vets:
            db.session.add(vet)
        db.session.commit()
        print(f"✓ Added {len(vets)} veterinarians")
    
    # Get pets from shelter system
    with shelter_app.app_context():
        pets = Pet.query.all()
        print(f"✓ Found {len(pets)} pets in shelter system")
    
    # Create health records for each pet
    with app.app_context():
        record_count = 0
        for pet in pets:
            # Generate vaccination history
            age_months = pet.age * 12 if pet.age else 12
            vaccinations = generate_vaccination_history(pet.species, age_months)
            deworming = generate_deworming_history(age_months)
            
            # Create health record
            last_checkup = datetime.now() - timedelta(days=random.randint(7, 90))
            
            record = VetRecord(
                pet_id=pet.id,
                pet_name=pet.name,
                species=pet.species,
                breed=pet.breed,
                owner_name='Shelter',
                owner_phone='555-SHELTER',
                owner_email='shelter@example.com',
                last_checkup=last_checkup,
                weight=round(random.uniform(5.0, 40.0), 1) if pet.species == 'dog' else round(random.uniform(3.0, 8.0), 1),
                temperature=round(random.uniform(38.0, 39.2), 1),  # Normal range for dogs/cats in Celsius
                heart_rate=random.randint(60, 140),
                respiratory_rate=random.randint(15, 30),
                body_condition_score=random.choice(['4/9', '5/9', '6/9']),
                microchip_number=f"USA{random.randint(100000000000, 999999999999)}",
                spayed_neutered=pet.spayed_neutered if hasattr(pet, 'spayed_neutered') else True,
                spay_neuter_date=datetime.now() - timedelta(days=random.randint(180, 730)),
                vaccinations=json.dumps(vaccinations),
                deworming_records=json.dumps(deworming),
                notes=f"Healthy {pet.species}. Regular checkup completed. All vaccinations up to date.",
                medical_history=random.choice([
                    'No significant medical history',
                    'History of ear infection at 6 months, resolved',
                    'Minor skin allergy, managed with diet',
                    'No known medical issues'
                ]),
                surgical_history='Spay/Neuter surgery' if pet.spayed_neutered else 'None',
                medications=random.choice(['None', 'Monthly heartworm prevention', 'Flea/tick prevention monthly']),
                allergies=random.choice(['None known', 'Chicken sensitivity', 'Seasonal allergies', 'None']),
                chronic_conditions='None',
                dental_health=random.choice(['Excellent', 'Good', 'Fair']),
                dental_cleaning_date=last_checkup if random.random() > 0.7 else None,
                heartworm_status='Negative',
                heartworm_test_date=last_checkup,
                flea_tick_prevention=True,
                flea_tick_product=random.choice(['Frontline Plus', 'Bravecto', 'Simparica', 'NexGard', 'Revolution']),
                flea_tick_last_applied=datetime.now() - timedelta(days=random.randint(1, 30)),
                updated_by=random.randint(1, 3)
            )
            
            db.session.add(record)
            record_count += 1
            
            # Create upcoming appointment for some pets (30% chance)
            if random.random() > 0.7:
                appointment_date = datetime.now() + timedelta(days=random.randint(7, 60))
                appointment = Appointment(
                    pet_id=pet.id,
                    pet_name=pet.name,
                    owner_name='Shelter',
                    owner_email='shelter@example.com',
                    owner_phone='555-SHELTER',
                    vet_id=random.randint(1, 3),
                    date=appointment_date,
                    duration=30,
                    reason=random.choice([
                        'Annual checkup',
                        'Vaccination booster',
                        'Dental cleaning',
                        'Follow-up examination',
                        'Pre-adoption checkup'
                    ]),
                    status='scheduled'
                )
                db.session.add(appointment)
        
        db.session.commit()
        
        total_records = VetRecord.query.count()
        total_appointments = Appointment.query.count()
        
        print(f"\n{'='*60}")
        print(f"✓ Successfully populated veterinary system!")
        print(f"  Health Records Created: {total_records}")
        print(f"  Upcoming Appointments: {total_appointments}")
        print(f"  Veterinarians: {len(vets)}")
        print(f"\n  All pets have comprehensive vaccination records including:")
        print(f"  - Core vaccinations (DHPP/FVRCP, Rabies)")
        print(f"  - Non-core vaccinations (varied)")
        print(f"  - Complete deworming history")
        print(f"  - Physical exam results")
        print(f"  - Preventive care records")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    populate_health_records()
