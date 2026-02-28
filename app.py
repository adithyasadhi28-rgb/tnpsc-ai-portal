import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="TNPSC Assistant", page_icon="🎤")

# --- SECURE API KEY ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Admin: Please add GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

st.title("🎤 TNPSC Voice Assistant")
st.info("Tap the box below and use your phone's keyboard microphone to speak!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- THE INPUT FIX ---
# We use a container to keep the chat input at the bottom
if prompt := st.chat_input("Ask about TNPSC (e.g., 'Who is the Governor?')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Immediately show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a TNPSC tutor. Provide clear, exam-oriented answers."},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")