"""
Recreate shelter database with new schema
"""
import os
import sys

# Delete old database
db_path = 'instance/shelter_system.db'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✓ Deleted {db_path}")
    except Exception as e:
        print(f"✗ Could not delete {db_path}: {e}")
        print("Please stop the shelter system first (Ctrl+C in its terminal)")
        sys.exit(1)

# Create new database
from shelter_system.app import app, db

with app.app_context():
    db.create_all()
    print("✓ Created new database with updated schema")
    print("\nRun: python populate_pets.py")
