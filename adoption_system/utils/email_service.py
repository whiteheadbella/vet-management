"""
Email service for sending notifications
"""
from flask import render_template
from flask_mail import Message, Mail
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mail = Mail()

def send_email(to, subject, template=None, **kwargs):
    """
    Send email using Flask-Mail
    
    Args:
        to: Recipient email address
        subject: Email subject
        template: Path to email template (optional)
        **kwargs: Additional template variables
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to
        )
        
        if template:
            # Render HTML template
            msg.html = render_template(template, **kwargs)
            # Also send plain text version
            msg.body = f"Subject: {subject}\n\n"
            for key, value in kwargs.items():
                msg.body += f"{key}: {value}\n"
        else:
            # Plain text email
            msg.body = kwargs.get('body', '')
        
        mail.send(msg)
        
        # Log notification in database
        from models import Notification, db
        if 'user_id' in kwargs:
            notification = Notification(
                user_id=kwargs['user_id'],
                notification_type='email',
                subject=subject,
                message=msg.body,
                status='sent'
            )
            db.session.add(notification)
            db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        
        # Log failed notification
        try:
            from models import Notification, db
            if 'user_id' in kwargs:
                notification = Notification(
                    user_id=kwargs['user_id'],
                    notification_type='email',
                    subject=subject,
                    message=str(e),
                    status='failed'
                )
                db.session.add(notification)
                db.session.commit()
        except:
            pass
        
        return False


def send_adoption_confirmation(user_email, user_name, pet_name, application_id):
    """Send adoption application confirmation email"""
    return send_email(
        to=user_email,
        subject='Adoption Application Received',
        template='emails/application_received.html',
        name=user_name,
        pet_name=pet_name,
        application_id=application_id
    )


def send_application_status_update(user_email, user_name, pet_name, status, notes=''):
    """Send application status update email"""
    template = f'emails/application_{status}.html'
    return send_email(
        to=user_email,
        subject=f'Adoption Application {status.title()}',
        template=template,
        name=user_name,
        pet_name=pet_name,
        notes=notes
    )


def send_appointment_reminder(user_email, user_name, pet_name, appointment_date, vet_name):
    """Send vet appointment reminder"""
    return send_email(
        to=user_email,
        subject='Veterinary Appointment Reminder',
        template='emails/appointment_reminder.html',
        name=user_name,
        pet_name=pet_name,
        appointment_date=appointment_date,
        vet_name=vet_name
    )


def send_welcome_email(user_email, user_name):
    """Send welcome email to new users"""
    return send_email(
        to=user_email,
        subject='Welcome to Pet Adoption System',
        template='emails/welcome.html',
        name=user_name
    )
