"""
Central configuration file for all three systems
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 3600)))
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))
    
    # Pagination
    PETS_PER_PAGE = int(os.getenv('PETS_PER_PAGE', 12))
    RECORDS_PER_PAGE = int(os.getenv('RECORDS_PER_PAGE', 20))
    
    # System URLs
    ADOPTION_SYSTEM_URL = os.getenv('ADOPTION_SYSTEM_URL', 'http://localhost:5000')
    SHELTER_SYSTEM_URL = os.getenv('SHELTER_SYSTEM_URL', 'http://localhost:5001')
    VETERINARY_SYSTEM_URL = os.getenv('VETERINARY_SYSTEM_URL', 'http://localhost:5002')
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # API Keys
    CAT_API_KEY = os.getenv('CAT_API_KEY', '')
    DOG_API_KEY = os.getenv('DOG_API_KEY', '')  # Not needed for dog.ceo
    
    # Google Calendar
    GOOGLE_CALENDAR_CREDENTIALS_FILE = os.getenv('GOOGLE_CALENDAR_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_CALENDAR_TOKEN_FILE = os.getenv('GOOGLE_CALENDAR_TOKEN_FILE', 'token.json')
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


class AdoptionSystemConfig(Config):
    """Configuration for Adoption System"""
    SQLALCHEMY_DATABASE_URI = os.getenv('ADOPTION_DB_URI', 'sqlite:///adoption_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ShelterSystemConfig(Config):
    """Configuration for Shelter Inventory System"""
    SQLALCHEMY_DATABASE_URI = os.getenv('SHELTER_DB_URI', 'sqlite:///shelter_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class VeterinarySystemConfig(Config):
    """Configuration for Veterinary Management System"""
    SQLALCHEMY_DATABASE_URI = os.getenv('VETERINARY_DB_URI', 'sqlite:///veterinary_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
