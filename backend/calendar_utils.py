import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

if os.getenv("RENDER"):
    SERVICE_ACCOUNT_FILE = "/etc/secrets/service_account.json"
else:
    SERVICE_ACCOUNT_FILE = '/ayojan-ai/credentials/service_account.json'
    
SCOPES = ['https://www.googleapis.com/auth/calendar']

CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def get_available_slots(date: str):
    start_of_day = f"{date}T00:00:00Z"
    end_of_day = f"{date}T23:59:59Z"

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    booked_times = []
    for event in events:
        start_time = event["start"].get("dateTime", "")
        if start_time:
            booked_times.append(start_time[:16])

    # Define working hours
    working_hours = [f"{date}T{hour:02d}:00" for hour in range(1, 24)]  # 1AM to 11PM

    available_slots = []
    for slot in working_hours:
        if slot not in booked_times:
            available_slots.append(slot)

    return available_slots


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
