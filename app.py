from typing import Any
import streamlit as st
import tempfile
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Summarize function
def summarize_audio(audio_file_path) -> Any:
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    audio_file = genai.upload_file(path=audio_file_path)
    response = model.generate_content(["Please summarize the following audio:", audio_file])
    return response.text

# Save uploaded audio
def save_uploaded_file(uploaded_file) -> Any | None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None

# --- Page Config ---
st.set_page_config(page_title="🎙️ Audio Summarizer", page_icon="🎧", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #00BFFF;
            margin-top: 10px;
        }
        .sub-text {
            text-align: center;
            font-size: 16px;
            color: #cccccc;
            margin-bottom: 30px;
        }
        .stTextInput, .stFileUploader, .stTextArea {
            background-color: #1e1e1e !important;
        }
        .stButton > button {
            background-color: #00BFFF;
            color: white;
            padding: 0.6em 2em;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #009ACD;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown('<div class="main-title">🎙️ Yash Audio Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Convert long audio into short, smart summaries using AI ⚡</div>', unsafe_allow_html=True)

with st.expander("ℹ️ About this App", expanded=False):
    st.markdown("""
    This app uses Google's **Gemini 1.5 Pro** model to intelligently summarize `.wav` or `.mp3` audio files.  
    Upload your audio and get a human-like summary in seconds!  
    Ideal for podcasts, interviews, meetings, lectures & more.
    """)

# File Upload
audio_file = st.file_uploader("🎵 Upload Your Audio File", type=['wav', 'mp3'])

# If file is uploaded
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)
    st.success("✅ File uploaded successfully!")

    if st.button("🔍 Summarize Audio"):
        with st.spinner("🧠 Generating summary..."):
            summary_text = summarize_audio(audio_path)
        st.success("✅ Summary Ready!")
        st.markdown("### 📄 Summary Output:")
        st.info(summary_text)
else:
    st.warning("📂 Please upload an audio file to begin.")
