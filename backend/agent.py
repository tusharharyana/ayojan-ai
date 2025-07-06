import os
import google.generativeai as genai
from dotenv import load_dotenv
from calendar_utils import get_available_slots, book_slot
from datetime import datetime
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def run_gemini_agent(message: str):
    try:
        today_str = datetime.today().strftime("%Y-%m-%d")

        # Step 1: Ask Gemini to extract intent, date, time, title
        prompt = f"""
            Today is {today_str}.

            You are a meeting assistant. From this user message, extract:
            1. Intent (book/view slots)
            2. Date in YYYY-MM-DD
            3. Time in HH:MM (24hr format)
            4. Meeting title (optional)

            Message: {message}

            Return only this format:
            intent: <view/book>
            date: <YYYY-MM-DD>
            time: <HH:MM>
            title: <optional>
            """

        response = model.generate_content(prompt)
        parsed = response.text.strip()

        # Extract using regex
        intent = re.search(r"intent:\s*(\w+)", parsed).group(1).lower()
        date = re.search(r"date:\s*([\d\-]+)", parsed).group(1)
        time = re.search(r"time:\s*([\d:]+)", parsed).group(1)
        title_match = re.search(r"title:\s*(.+)", parsed)
        title = title_match.group(1) if title_match else "AyojanAI Booking"

        datetime_str = f"{date}T{time}:00"

        if intent == "book":
            link = book_slot(datetime_str, title)
            return f"Booked your meeting: **{title}** on `{date}` at `{time}`. [View it]({link})"
        elif intent == "view":
            slots = get_available_slots(date)
            return f"Available slots on {date}:\n" + "\n".join([f"- {s}" for s in slots])
        else:
            return "I didn't understand the intent. Please say if you want to book or view slots."

    except Exception as e:
        return f"Error: {str(e)}"
