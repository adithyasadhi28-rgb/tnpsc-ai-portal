import streamlit as st
from groq import Groq
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="TNPSC AI Portal", page_icon="📚")

# --- SECURE API KEY ---
# This pulls the key from Streamlit Cloud Secrets (the hidden vault)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Admin: Please add GROQ_API_KEY to the Streamlit Secrets dashboard.")
    st.stop()

client = Groq(api_key=api_key)

# --- APP INTERFACE ---
st.title("🚀 TNPSC Exam AI Portal")
st.subheader("Generate Quizzes & Explanations Instantly")

topic = st.text_input("Enter Topic (e.g., Indian Economy, Mughal Empire):")

if st.button("Generate Quiz"):
    if topic:
        with st.spinner("AI is thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a TNPSC exam expert. Create 3 multiple choice questions with explanations."},
                        {"role": "user", "content": f"Generate a quiz on: {topic}"}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.markdown(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a topic first!")