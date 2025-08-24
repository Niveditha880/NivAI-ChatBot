import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import datetime



# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Expert modes and system prompts
EXPERT_MODES = {
    "Developer Assistant": "You are a coding assistant. Help the user write, debug, and explain code.",
    "Travel Planner": "You are a travel planner. Help the user choose destinations, plan trips, and provide travel tips.",
    "Therapist Bot": "You are a compassionate and non-judgmental listener. Offer emotional support and mental wellness advice.",
    "Math Solver": "You are a math expert. Solve math problems step-by-step with clear explanations.",
    "Interview Coach": "You are an experienced interview coach. Provide job interview tips, questions, and feedback."
}

# Set Streamlit page config
st.set_page_config(page_title="NivAI Chatbot", page_icon="🧠", layout="centered")
st.title("🤖 NivAI - Conversations Redefined")

# Sidebar for mode selection and download
st.sidebar.title("🛠️ Expert Mode")
selected_mode = st.sidebar.selectbox("Choose Mode", list(EXPERT_MODES.keys()))
st.sidebar.info(f"You're chatting with **{selected_mode}** mode.")

# Optional: Download chat history
if st.sidebar.button("📥 Download Chat History"):
    chat_text = ""
    for msg in st.session_state.get("chat_session", {}).get("history", []):
        role = "You" if msg.role == "user" else "NivAI"
        chat_text += f"{role}: {msg.parts[0].text}\n\n"
    st.sidebar.download_button("Download .txt", chat_text, file_name="nivai_chat.txt")

# Reset chat if mode changed or not set
if "chat_session" not in st.session_state or st.session_state.get("current_mode") != selected_mode:
    model = genai.GenerativeModel("gemini-1.5-flash-002")
    system_instruction=EXPERT_MODES[selected_mode]
        

    st.session_state.chat_session = model.start_chat(
        history=[],
    )

    st.session_state.current_mode = selected_mode
    st.session_state.welcome_shown = False  # reset welcome message

# Welcome message
if not st.session_state.get("welcome_shown"):
    st.info(f"👋 Welcome to NivAI! You're now talking to a **{selected_mode}**.")
    st.session_state.welcome_shown = True

# Display chat history
for msg in st.session_state.chat_session.history:
    role = "assistant" if msg.role == "model" else "user"
    avatar = "🤖" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.parts[0].text)

# Chat input box
user_input = st.chat_input("Ask NivAI...")
if user_input:
    st.chat_message("user", avatar="👤").markdown(user_input)

    # Get current system date & time
    current_time = datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S")

    # Inject into prompt
    prompt = f"Current real-world date and time is {current_time}. Use this when answering date/time related questions.\n\nUser: {user_input}"

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("NivAI is thinking..."):
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)

    # Welcome message
if not st.session_state.get("welcome_shown"):
        st.info(f"👋 Welcome to NivAI! You're now talking to a **{selected_mode}**.")
    
    # ✅ Add disclaimer for Therapist mode
if selected_mode == "Therapist Bot":
        st.warning("⚠️ Note: I’m an AI, not a licensed professional. For serious concerns, please consult a qualified therapist.")
    
st.session_state.welcome_shown = True



# Custom footer
st.markdown("""---""")
st.markdown("🔧 Built with 💙 using **Gemini API** & **Streamlit** | © 2025 NivAI")
