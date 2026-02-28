import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="TNPSC AI Assistant", page_icon="🎤")

# --- SECURE API KEY ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Admin: Missing API Key")
    st.stop()

client = Groq(api_key=api_key)

# --- CHAT INTERFACE ---
st.title("🎤 TNPSC Voice Assistant")
st.write("Ask questions about TNPSC or generate a quiz!")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (This works with smartphone voice-to-text microphones)
# When a user taps the microphone icon on their mobile keyboard, it fills this box
if prompt := st.chat_input("Type or use your phone's mic to ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is analyzing..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a TNPSC tutor. Answer questions or create quizzes based on the user's input."},
                    {"role": "user", "content": prompt}
                ]
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})