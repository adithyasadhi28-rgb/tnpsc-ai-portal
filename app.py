import streamlit as st
from groq import Groq
import json

# --- PAGE SETUP ---
st.set_page_config(page_title="Exam LeetCode 2026", layout="wide", page_icon="🏆")

# --- SECURE API KEY ---
# When you deploy, you'll put your key in Streamlit's "Secrets"
# For testing, you can paste it here or use an environment variable
GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key", type="password")

if not GROQ_API_KEY:
    st.info("💡 Please enter your Groq API Key (from console.groq.com) to start.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- AI ENGINES ---
def generate_quiz(topic):
    """Generates 3 MCQs using Llama 3.3 70B"""
    prompt = f"Create a 3-question MCQ quiz on {topic} for TNPSC/UPSC. Return ONLY the questions with options A-D and the correct answer."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def explain_concept(question):
    """Deep explanation engine"""
    prompt = f"Explain this exam question like a professional tutor: {question}"
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Faster model for explanations
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- MAIN UI ---
st.title("🎓 Exam LeetCode: Infinite Learning")
st.markdown("---")

menu = ["Quiz Mode", "AI Explainer", "Discussion (Coming Soon)"]
choice = st.sidebar.selectbox("Choose Module", menu)

if choice == "Quiz Mode":
    st.header("🎯 Practice Arena")
    topic = st.text_input("Enter Topic (e.g., 'Indian Polity', 'Ratios')", "Indian Constitution")
    
    if st.button("Generate Questions"):
        with st.spinner("AI is crafting unique questions..."):
            quiz_text = generate_quiz(topic)
            st.session_state['current_quiz'] = quiz_text
            st.markdown(quiz_text)

if choice == "AI Explainer":
    st.header("🧠 Concept Explainer")
    user_q = st.text_area("Paste a difficult question here:")
    if st.button("Explain Step-by-Step"):
        with st.spinner("Analyzing..."):
            explanation = explain_concept(user_q)
            st.success("Analysis Complete!")
            st.markdown(explanation)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("🟢 Server: Groq Cloud (Free Tier)")
st.sidebar.write("💻 Architecture: Streamlit + Llama 3")