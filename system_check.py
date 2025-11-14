"""
System Check - Verify all components are ready
"""
import os
import sys
import importlib.util

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_cors',
        'flask_mail',
        'requests',
        'werkzeug'
    ]
    
    all_ok = True
    for package in required:
        spec = importlib.util.find_spec(package)
        if spec is not None:
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} (Missing)")
            all_ok = False
    
    if not all_ok:
        print("\n  Install missing packages:")
        print("  pip install -r requirements.txt")
    
    return all_ok

def check_files():
    """Check if required files exist"""
    print("\nChecking project files...")
    required_files = [
        'requirements.txt',
        'config.py',
        '.env',
        'adoption_system/app.py',
        'adoption_system/models.py',
        'shelter_system/app.py',
        'shelter_system/models.py',
        'veterinary_system/app.py',
        'veterinary_system/models.py'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (Missing)")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    required_dirs = [
        'adoption_system/templates',
        'adoption_system/static/uploads',
        'shelter_system/static/uploads',
        'veterinary_system/static/uploads'
    ]
    
    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} (Missing)")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"    → Created {directory}")
            except:
                all_ok = False
    
    return all_ok

def check_databases():
    """Check if databases exist"""
    print("\nChecking databases...")
    databases = [
        ('adoption_system/adoption_system.db', 'Adoption System'),
        ('shelter_system/shelter_system.db', 'Shelter System'),
        ('veterinary_system/veterinary_system.db', 'Veterinary System')
    ]
    
    all_ok = True
    for db_file, name in databases:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"  ✓ {name} ({size} bytes)")
        else:
            print(f"  ✗ {name} (Not initialized)")
            all_ok = False
    
    if not all_ok:
        print("\n  Initialize databases:")
        print("  python init_databases.py")
    
    return all_ok

def check_env_config():
    """Check environment configuration"""
    print("\nChecking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("    Copy .env.example to .env")
        return False
    
    print("  ✓ .env file exists")
    
    # Read .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    # Check for placeholder values
    warnings = []
    if 'dev-secret-key' in content:
        warnings.append("SECRET_KEY is using default value")
    if 'your-email@gmail.com' in content:
        warnings.append("Email configuration not set")
    
    if warnings:
        print("\n  ⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"    • {warning}")
        print("  (System will work, but some features may be limited)")
    
    return True

def main():
    print("=" * 70)
    print("Pet Adoption System - System Check")
    print("=" * 70)
    print()
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_files(),
        check_directories(),
        check_env_config(),
        check_databases()
    ]
    
    print()
    print("=" * 70)
    
    if all(checks):
        print("✓ All checks passed! System is ready to run.")
        print()
        print("To start the system:")
        print("  python start_all.py")
        print()
        print("Or start each system individually:")
        print("  python adoption_system/app.py     (Port 5000)")
        print("  python shelter_system/app.py      (Port 5001)")
        print("  python veterinary_system/app.py   (Port 5002)")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print()
        if not checks[4] or not checks[5]:  # env or databases
            print("Quick fix:")
            if not checks[4]:
                print("  1. Copy .env.example to .env")
            if not checks[5]:
                print("  2. python init_databases.py")
    
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during system check: {e}")
        import traceback
        traceback.print_exc()
