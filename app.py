# --- SECURE API KEY ---
# This looks for the key you saved in the Streamlit "Secrets" dashboard
import os

if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # This is a fallback for local testing
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🔑 Admin: Please add the GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)