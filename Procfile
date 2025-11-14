web: gunicorn adoption_system.app:app --bind 0.0.0.0:$PORT --workers 2
shelter: gunicorn shelter_system.app:app --bind 0.0.0.0:$SHELTER_PORT --workers 2
veterinary: gunicorn veterinary_system.app:app --bind 0.0.0.0:$VETERINARY_PORT --workers 2
