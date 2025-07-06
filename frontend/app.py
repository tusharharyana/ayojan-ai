import streamlit as st
import requests

st.set_page_config(
    page_title="AyojanAI – Smart Meeting Assistant",
    page_icon="📅",
    layout="centered"
)

st.markdown("""
    <style>
        .stChatMessage {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
        }
        .user {
            background-color: #f0f8ff;
            text-align: right;
        }
        .assistant {
            background-color: #f9f9f9;
            text-align: left;
        }
        .title {
            text-align: center;
            color: #2C3E50;
            font-weight: bold;
        }
        .caption {
            text-align: center;
            color: gray;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='title'>AyojanAI ✨</h2>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Your AI-powered meeting assistant</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Welcome to **AyojanAI ✨**!\n\nI can help you book meetings or check availability. Try something like:\n- *Book a meeting tomorrow at 3 PM*\n- *Show available slots on Friday*"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_input = st.chat_input("Ask me to book or check meetings...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://localhost:8000/chat", json={"message": user_input}, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    bot_reply = data.get("response", "Unexpected response from server.")
                else:
                    bot_reply = "Server busy. Please try again shortly."
            except requests.exceptions.Timeout:
                bot_reply = "⏱Server timed out. Please try again later."
            except requests.exceptions.ConnectionError:
                bot_reply = "Cannot connect to server. Make sure FastAPI is running."
            except Exception as e:
                bot_reply = f"An error occurred: {str(e)}"

            st.markdown(bot_reply, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

st.divider()
st.markdown("<p style='text-align:center; font-size: 12px; color: #aaa;'>Made with ❤️ by Tushar · Powered by Gemini</p>", unsafe_allow_html=True)
