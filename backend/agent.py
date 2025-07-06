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

        prompt = f"""
            Today is {today_str}.

            You are a helpful meeting assistant. From this user message, extract:

            1. intent: 'view' or 'book'
            2. date: in YYYY-MM-DD format
            3. time: in HH:MM 24hr format (if relevant)
            4. title: short meeting title (if booking), or just say 'NA' if not applicable

            Message: {message}

            Return exactly in this format:
            intent: <book/view>
            date: <YYYY-MM-DD>
            time: <HH:MM>
            title: <Meeting title or NA>
            """


        response = model.generate_content(prompt)
        parsed = response.text.strip()

        # Extract intent
        intent_match = re.search(r"intent:\s*(\w+)", parsed)
        intent = intent_match.group(1).lower() if intent_match else "unknown"

        # Extract date
        date_match = re.search(r"date:\s*([\d\-]+)", parsed)
        date = date_match.group(1) if date_match else datetime.today().strftime("%Y-%m-%d")

        # Extract time
        time_match = re.search(r"time:\s*([\d:]+)", parsed)
        time = time_match.group(1) if time_match else "10:00"

        # Extract title
        title_match = re.search(r"title:\s*(.+)", parsed)
        title = title_match.group(1).strip() if title_match else "AyojanAI Booking"
        if title.lower() in ["<optional>", "optional", "none", ""]:
            title = "AyojanAI Booking"

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
