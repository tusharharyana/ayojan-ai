import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = '/ayojan-ai/credentials/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def get_available_slots(date: str):
    # Dummy logic
    slots = [
        f"{date}T10:00:00",
        f"{date}T11:00:00",
        f"{date}T15:00:00",
    ]
    return slots

def book_slot(start_time: str, summary: str = "AyojanAI Booking"):
    start = datetime.fromisoformat(start_time)
    end = start + timedelta(hours=1)
    
    event = {
        'summary': summary,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')
