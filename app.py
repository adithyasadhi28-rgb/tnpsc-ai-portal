import streamlit as st
from groq import Groq
import PyPDF2
import os

st.set_page_config(page_title="TNPSC Smart Tutor", page_icon="📖")

# --- API SETUP ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.title("📖 TNPSC Smart PDF Tutor")

# --- PDF UPLOADER SECTION ---
st.sidebar.header("Upload Study Material")
uploaded_file = st.sidebar.file_uploader("Upload a TNPSC PDF/Notes", type="pdf")

pdf_text = ""
if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()
    st.sidebar.success("✅ PDF Loaded Successfully!")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the PDF or a TNPSC topic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # If a PDF is uploaded, we tell the AI to use its content
    context = f"Use this text to answer: {pdf_text[:4000]}" if pdf_text else "You are a TNPSC expert."

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})