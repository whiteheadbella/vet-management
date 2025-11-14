"""
Google Calendar API integration
"""
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Google Calendar API will be initialized when credentials are available
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Google Calendar API not available. Install required packages.")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get Google Calendar service"""
    if not GOOGLE_AVAILABLE:
        return None
    
    from config import Config
    
    creds = None
    token_file = Config.GOOGLE_CALENDAR_TOKEN_FILE
    credentials_file = Config.GOOGLE_CALENDAR_CREDENTIALS_FILE
    
    # Check if token file exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print("Google Calendar credentials file not found.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_calendar_event(title, description, start_time, duration=30, attendees=None):
    """
    Create a Google Calendar event
    
    Args:
        title: Event title
        description: Event description
        start_time: datetime object for start time
        duration: Duration in minutes
        attendees: List of email addresses
    
    Returns:
        Event ID if successful, None otherwise
    """
    try:
        service = get_calendar_service()
        if not service:
            return None
        
        end_time = start_time + timedelta(minutes=duration)
        
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('id')
    
    except Exception as e:
        print(f"Error creating calendar event: {e}")
        return None


def update_calendar_event(event_id, title=None, description=None, start_time=None, duration=None):
    """Update a Google Calendar event"""
    try:
        service = get_calendar_service()
        if not service:
            return False
        
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        
        if title:
            event['summary'] = title
        if description:
            event['description'] = description
        if start_time:
            end_time = start_time + timedelta(minutes=duration or 30)
            event['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            }
            event['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            }
        
        updated_event = service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()
        
        return True
    
    except Exception as e:
        print(f"Error updating calendar event: {e}")
        return False


def delete_calendar_event(event_id):
    """Delete a Google Calendar event"""
    try:
        service = get_calendar_service()
        if not service:
            return False
        
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    
    except Exception as e:
        print(f"Error deleting calendar event: {e}")
        return False


def get_upcoming_events(max_results=10):
    """Get upcoming calendar events"""
    try:
        service = get_calendar_service()
        if not service:
            return []
        
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return events
    
    except Exception as e:
        print(f"Error getting events: {e}")
        return []
