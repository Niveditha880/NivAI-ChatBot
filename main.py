import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with NivAI!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.5-flash')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

    EXPERT_MODES = {
    "Developer Assistant": "You are a coding assistant. Help the user write, debug, and explain code.",
    "Travel Planner": "You are a travel planner. Help the user choose destinations, plan trips, and provide travel tips.",
    "Therapist Bot": "You are a compassionate and non-judgmental listener. Offer emotional support and mental wellness advice.",
    "Math Solver": "You are a math expert. Solve math problems step-by-step with clear explanations.",
    "Interview Coach": "You are an experienced interview coach. Provide job interview tips, questions, and feedback."
}


# Display the chatbot's title on the page
st.title("🤖 NivAI- Conversations Redefined")


st.sidebar.title("🛠️ Expert Mode")
selected_mode = st.sidebar.selectbox("Choose Chatbot Persona", list(EXPERT_MODES.keys()))
st.sidebar.info(f"Mode: **{selected_mode}**")

# Create or reset chat session
if "chat_session" not in st.session_state or st.session_state.get("current_mode") != selected_mode:
    st.session_state.chat_session = gen_ai.GenerativeModel("gemini-1.5-pro-latest").start_chat(
        history=[],
        system_instruction=EXPERT_MODES[selected_mode]
    )
    st.session_state.current_mode = selected_mode  # Track selected mode

# Display chat history
for msg in st.session_state.chat_session.history:
    role = "assistant" if msg.role == "model" else msg.role
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# Chat input
user_input = st.chat_input("Ask NivAI...")
if user_input:
    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("NivAI is thinking..."):
            response = st.session_state.chat_session.send_message(user_input)
            st.markdown(response.text)



# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask NivAI...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)