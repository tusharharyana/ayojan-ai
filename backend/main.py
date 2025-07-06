from fastapi import FastAPI, Request
from pydantic import BaseModel
from calendar_utils import get_available_slots, book_slot
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AyojanAI Backend is Running ✅"}

@app.get("/slots")
def get_slots(date: str = None):
    if not date:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    slots = get_available_slots(date)
    return {"date": date, "slots": slots}

class BookingRequest(BaseModel):
    start_time: str
    summary: str = "AyojanAI Meeting"

@app.post("/book")
def book_meeting(req: BookingRequest):
    link = book_slot(req.start_time, req.summary)
    return {"status": "booked", "link": link}
