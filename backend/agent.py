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

        # Extract intent, date, time, title
        intent = re.search(r"intent:\s*(\w+)", parsed)
        date = re.search(r"date:\s*([\d\-]+)", parsed)
        time = re.search(r"time:\s*([\d:]+)", parsed)
        title = re.search(r"title:\s*(.+)", parsed)

        intent = intent.group(1).lower() if intent else "unknown"
        date = date.group(1) if date else today_str
        time = time.group(1) if time else "10:00"
        title = title.group(1).strip() if title else "AyojanAI Booking"

        if title.lower() in ["<optional>", "optional", "na", "none", ""]:
            title = "AyojanAI Booking"

        datetime_str = f"{date}T{time}:00"

        if intent == "book":
            link = book_slot(datetime_str, title)
            return f""" 
                ✅ **Meeting Booked Successfully**

                **Title:** {title}  
                **Date:** `{date}`  
                **Time:** `{time}`  

                🔗 [Click here to view it in your calendar]({link})
                """

        elif intent == "view":
            slots = get_available_slots(date)
            if not slots:
                return f"📅 **No available slots on `{date}`.** Try a different day."

            slot_list = "\n".join([f"• `{s[-5:]}`" for s in slots])
            return f"""\
            📅 **Available Slots on `{date}`**  
            {slot_list}
            """

        else:
            return (
                "I couldn't understand your request.\n\n"
                "Try saying:\n"
                "- `Book a meeting tomorrow at 3 PM`\n"
                "- `Check slots for Friday`"
            )

    except Exception as e:
        return f"❌ **Error:** {str(e)}"
