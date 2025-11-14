"""
User profile routes
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('profile', __name__, url_prefix='/profile')

from adoption_system.models import AdoptionApplication, AdoptedPet, Notification

@bp.route('/')
@login_required
def index():
    """View user profile"""
    return render_template('profile/index.html')


@bp.route('/notifications')
@login_required
def notifications():
    """View user notifications"""
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.sent_at.desc()).all()
    
    return render_template('profile/notifications.html', notifications=notifications)


@bp.route('/settings')
@login_required
def settings():
    """User settings"""
    return render_template('profile/settings.html')
