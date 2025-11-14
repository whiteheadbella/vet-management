"""
Startup script to launch all three systems
Run this to start the entire Pet Adoption System
"""
import subprocess
import sys
import os
import time

def start_system(name, port, directory):
    """Start a system in a new terminal window"""
    print(f"Starting {name} on port {port}...")
    
    if sys.platform == 'win32':
        # Windows
        cmd = f'start cmd /k "cd {directory} && python app.py"'
        subprocess.Popen(cmd, shell=True)
    else:
        # Mac/Linux
        cmd = f"cd {directory} && python app.py"
        subprocess.Popen(cmd, shell=True)
    
    time.sleep(2)

def main():
    print("=" * 60)
    print("Pet Adoption System - Startup Script")
    print("=" * 60)
    print()
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if virtual environment exists
    venv_path = os.path.join(base_dir, 'venv')
    if not os.path.exists(venv_path):
        print("⚠️  Virtual environment not found!")
        print("Please create it first:")
        print("  python -m venv venv")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("  pip install -r requirements.txt")
        return
    
    # Check if databases exist
    adoption_db = os.path.join(base_dir, 'adoption_system', 'adoption_system.db')
    shelter_db = os.path.join(base_dir, 'shelter_system', 'shelter_system.db')
    vet_db = os.path.join(base_dir, 'veterinary_system', 'veterinary_system.db')
    
    if not all([os.path.exists(adoption_db), os.path.exists(shelter_db), os.path.exists(vet_db)]):
        print("⚠️  Databases not initialized!")
        print("Please run: python init_databases.py")
        print()
        response = input("Would you like to initialize databases now? (y/n): ")
        if response.lower() == 'y':
            print("Initializing databases...")
            subprocess.run([sys.executable, 'init_databases.py'])
            print()
        else:
            return
    
    print("Starting all systems...")
    print()
    
    # Start all three systems
    systems = [
        ("Adoption System", 5000, os.path.join(base_dir, 'adoption_system')),
        ("Shelter System", 5001, os.path.join(base_dir, 'shelter_system')),
        ("Veterinary System", 5002, os.path.join(base_dir, 'veterinary_system'))
    ]
    
    for name, port, directory in systems:
        start_system(name, port, directory)
    
    print()
    print("=" * 60)
    print("All systems started!")
    print("=" * 60)
    print()
    print("Access the systems at:")
    print("  • Adoption System:    http://localhost:5000")
    print("  • Shelter System:     http://localhost:5001")
    print("  • Veterinary System:  http://localhost:5002")
    print()
    print("Default login credentials:")
    print("  Adopter:  adopter@example.com / password123")
    print("  Shelter:  shelter@example.com / password123")
    print("  Vet:      vet@example.com / password123")
    print()
    print("Press Ctrl+C in each terminal window to stop the systems.")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown initiated...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the error message and try again.")
