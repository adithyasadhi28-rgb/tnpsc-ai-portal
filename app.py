import streamlit as st
import os
from groq import Groq

# --- SECURE API KEY (Cloud Method) ---
# This pulls the key from Streamlit Cloud Secrets automatically
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Fallback for your ASUS TUF local testing
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ Admin: GROQ_API_KEY not found in Secrets. Please add it in App Settings.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)