"""
Initialize all databases for the Pet Adoption System
Run this script to set up all three system databases
"""
import sys
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_adoption_system():
    """Initialize Adoption System database"""
    print("\n=== Initializing Adoption System Database ===")
    try:
        # Add adoption system to path
        adoption_path = os.path.join(BASE_DIR, 'adoption_system')
        if adoption_path not in sys.path:
            sys.path.insert(0, adoption_path)
        
        # Import from adoption system
        from adoption_system.app import app, db
        from adoption_system.models import User, AdoptionApplication, AdoptedPet, Notification
        
        with app.app_context():
            db.create_all()
            print("✓ Adoption System database tables created")
        
        return True
    except Exception as e:
        print(f"✗ Error initializing Adoption System: {e}")
        import traceback
        traceback.print_exc()
        return False


def init_shelter_system():
    """Initialize Shelter System database"""
    print("\n=== Initializing Shelter System Database ===")
    try:
        # Add shelter system to path
        shelter_path = os.path.join(BASE_DIR, 'shelter_system')
        if shelter_path not in sys.path:
            sys.path.insert(0, shelter_path)
        
        # Import from shelter system
        from shelter_system.app import app, db
        from shelter_system.models import Pet, PetImage, ShelterLog
        
        with app.app_context():
            db.create_all()
            print("✓ Shelter System database tables created")
        
        return True
    except Exception as e:
        print(f"✗ Error initializing Shelter System: {e}")
        import traceback
        traceback.print_exc()
        return False


def init_veterinary_system():
    """Initialize Veterinary System database"""
    print("\n=== Initializing Veterinary System Database ===")
    try:
        # Add veterinary system to path
        vet_path = os.path.join(BASE_DIR, 'veterinary_system')
        if vet_path not in sys.path:
            sys.path.insert(0, vet_path)
        
        # Import from veterinary system
        from veterinary_system.app import app, db
        from veterinary_system.models import Vet, VetRecord, Appointment
        
        with app.app_context():
            db.create_all()
            print("✓ Veterinary System database tables created")
        
        return True
    except Exception as e:
        print(f"✗ Error initializing Veterinary System: {e}")
        import traceback
        traceback.print_exc()
        return False


def seed_sample_data():
    """Seed all systems with sample data"""
    print("\n=== Seeding Sample Data ===")
    
    # Seed Adoption System
    try:
        from adoption_system.app import app, db
        from adoption_system.models import User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            if User.query.count() == 0:
                users = [
                    User(name='John Adopter', email='adopter@example.com',
                         password=generate_password_hash('password123'), role='adopter'),
                    User(name='Shelter Manager', email='shelter@example.com',
                         password=generate_password_hash('password123'), role='shelter'),
                    User(name='Dr. Veterinarian', email='vet@example.com',
                         password=generate_password_hash('password123'), role='vet'),
                ]
                for user in users:
                    db.session.add(user)
                db.session.commit()
                print("✓ Sample users created")
    except Exception as e:
        print(f"✗ Error seeding adoption system: {e}")
        import traceback
        traceback.print_exc()
    
    # Seed Shelter System
    try:
        from shelter_system.app import app, db
        from shelter_system.models import Pet
        
        with app.app_context():
            if Pet.query.count() == 0:
                sample_pets = [
                    Pet(name='Max', species='dog', breed='Golden Retriever', age=2, gender='male',
                        description='Friendly and energetic golden retriever', status='available',
                        vaccinated=True, spayed_neutered=True, adoption_fee=200.0),
                    Pet(name='Bella', species='cat', breed='Siamese', age=1, gender='female',
                        description='Playful and affectionate siamese cat', status='available',
                        vaccinated=True, spayed_neutered=True, adoption_fee=150.0),
                    Pet(name='Charlie', species='dog', breed='Beagle', age=3, gender='male',
                        description='Calm and loving beagle', status='available',
                        vaccinated=True, spayed_neutered=True, adoption_fee=180.0),
                ]
                for pet in sample_pets:
                    db.session.add(pet)
                db.session.commit()
                print("✓ Sample pets created")
    except Exception as e:
        print(f"✗ Error seeding shelter system: {e}")
        import traceback
        traceback.print_exc()
    
    # Seed Veterinary System
    try:
        from veterinary_system.app import app, db
        from veterinary_system.models import Vet
        
        with app.app_context():
            if Vet.query.count() == 0:
                vets = [
                    Vet(name='Dr. Sarah Johnson', email='sarah@vetclinic.com',
                        specialization='General Practice', phone='555-0101'),
                    Vet(name='Dr. Michael Chen', email='michael@vetclinic.com',
                        specialization='Surgery', phone='555-0102'),
                ]
                for vet in vets:
                    db.session.add(vet)
                db.session.commit()
                print("✓ Sample vets created")
    except Exception as e:
        print(f"✗ Error seeding veterinary system: {e}")
        import traceback
        traceback.print_exc()


def create_upload_directories():
    """Create upload directories for all systems"""
    print("\n=== Creating Upload Directories ===")
    directories = [
        os.path.join(BASE_DIR, 'adoption_system', 'static', 'uploads'),
        os.path.join(BASE_DIR, 'shelter_system', 'static', 'uploads'),
        os.path.join(BASE_DIR, 'veterinary_system', 'static', 'uploads')
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            # Create .gitkeep file
            with open(os.path.join(directory, '.gitkeep'), 'w') as f:
                f.write('')
            print(f"✓ Created {directory}")
        except Exception as e:
            print(f"✗ Error creating {directory}: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("Pet Adoption System - Database Initialization")
    print("=" * 60)
    
    # Create upload directories
    create_upload_directories()
    
    # Initialize databases
    adoption_ok = init_adoption_system()
    shelter_ok = init_shelter_system()
    veterinary_ok = init_veterinary_system()
    
    # Seed data if initialization was successful
    if adoption_ok and shelter_ok and veterinary_ok:
        seed_sample_data()
    
    print("\n" + "=" * 60)
    print("Initialization Complete!")
    print("=" * 60)
    print("\nSample Login Credentials:")
    print("  Adopter:  adopter@example.com / password123")
    print("  Shelter:  shelter@example.com / password123")
    print("  Vet:      vet@example.com / password123")
    print("\nTo start the systems:")
    print("  1. Adoption System:   python adoption_system/app.py")
    print("  2. Shelter System:    python shelter_system/app.py")
    print("  3. Veterinary System: python veterinary_system/app.py")
    print("=" * 60)
