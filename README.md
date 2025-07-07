# 📅 AyojanAI – Smart Calendar Assistant

AyojanAI is a conversational AI-powered assistant that helps you book and manage meetings using natural language. It uses Gemini AI and Google Calendar API to understand your intent and automatically create calendar events.


---

## 🚀 Features

- 🤖 Powered by Gemini (Google's LLM)
- 📆 Book meetings or check available slots via chat
- ⚙️ Google Calendar API integration
- 🌐 FastAPI backend + Streamlit frontend
- 🔒 Secure `.env` + credential handling

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI**: Gemini Pro (`google-generativeai`)
- **Calendar API**: Google Calendar (via Service Account)
- **Deployment**: Render (backend) + Streamlit Cloud (frontend)

---

## Project Structure
```bash
ayojan-ai/
├── backend/
│ ├── main.py
│ ├── agent.py
│ ├── calendar_utils.py
│ ├── requirements.txt
│ ├── credentials/
│ │ └── service_account.json ← 🔐 Your calendar credentials
│ └── .env ← 🔐 Your GOOGLE_CALENDAR_ID, GEMINI_API_KEY, BACKEND_URL
├── frontend/
│ ├── app.py
│ ├── requirements.txt
│ └── .streamlit/
│ └── secrets.toml
```

---

## Setup Guide

### 1. Clone the repo
```bash
git clone https://github.com/tusharharyana/ayojan-ai.git
cd ajoyan-ai
```

## 2. Backend Setup


```bash
python -m venv venv
venv\Scripts\activate
```
```bash
cd backend
pip install -r requirements.txt
```
🔸 Inside `/backend/`, create a `credentials` folder:

🔸 Add your Google service account key:
File name: `service_account.json`

File path: `/ayojan-ai/backend/credentials/service_account.json`

🔸 Add a `.env` file inside `backend/` with:
```bash
GOOGLE_CALENDAR_ID=
GEMINI_API_KEY=
BACKEND_URL=http://localhost:8000
```
- Never commit `service_account.json` or `.env` — they’re ignored in `.gitignore`.

## 3. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
```

## 4. Run the App Locally
Start Backend
```bash
uvicorn main:app --reload
```

Start Frontend
```bash
streamlit run app.py
```

## ✨ Future Improvements
- 🔐 OAuth2 calendar support for individual users
- 📬 Email reminders or summaries
- 🗓️ UI to list/cancel events
- 📊 Analytics dashboard
