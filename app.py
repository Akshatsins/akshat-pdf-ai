import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from utils import extract_text_from_pdf
from chat_logic import ask_document


st.set_page_config(
    page_title="Akshat's PDF AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* 1. Main Dark Background */
    .stApp {
        background-color: #0F172A; /* Deep Slate Blue - Easy on eyes */
        color: #E2E8F0; /* Soft White Text */
        font-family: 'Inter', sans-serif;
    }
    
    /* 2. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B; /* Slightly lighter slate */
        border-right: 1px solid #334155;
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #94A3B8 !important;
    }
    
    /* 3. Chat Message Bubbles (Dark Mode Optimized) */
    .stChatMessage {
        background-color: transparent;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* User Message - Gradient Blue/Purple */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        border: none;
        color: white;
    }
    
    /* Assistant Message - Dark Card */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #1E293B;
        border: 1px solid #334155;
        color: #E2E8F0;
    }
    
    /* 4. Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(left, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* 5. Custom Button Styling (Neon Glow) */
    .stButton>button {
        background: linear-gradient(90deg, #06B6D4 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(6, 182, 212, 0.39);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.23);
    }
    
    /* 6. Input Fields (Dark Theme) */
    .stTextInput>div>div>input {
        background-color: #1E293B;
        color: white;
        border: 1px solid #475569;
        border-radius: 10px;
    }
    
    /* 7. File Uploader Styling */
    [data-testid="stFileUploader"] {
        background-color: #1E293B;
        border: 2px dashed #475569;
        border-radius: 15px;
        padding: 20px;
    }
    [data-testid="stFileUploader"] small {
        color: #94A3B8;
    }
    
    /* Hide the default Streamlit header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-header">Akshat\'s PDF AI 🌌</div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #94A3B8; margin-bottom: 30px; font-size: 1.1rem;'>
    Your Intelligent Dark-Mode Document Assistant. Powered by Groq.
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### ⚙️ System Control")
    
    if os.environ.get("GROQ_API_KEY"):
        st.success("🟢 System Online")
    else:
        st.warning("🔴 System Offline")
        api_key = st.text_input("Enter API Key", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 📝 Status Log")
    if "doc_text" in st.session_state and st.session_state.doc_text:
        st.info("📄 Document Loaded")
    else:
        st.info("Waiting for PDF...")
    
    st.markdown("---")
    if st.button("🗑️ Reset Memory"):
        st.session_state.chat_history = []
        st.session_state.doc_text = None
        st.rerun()


if "doc_text" not in st.session_state:
    st.session_state.doc_text = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if st.session_state.doc_text is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("📂 Upload your PDF here", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("🌑 Analyzing in the dark..."):
                file_bytes = uploaded_file.read()
                text = extract_text_from_pdf(file_bytes)
                st.session_state.doc_text = text
                st.rerun()
else:
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    
    st.markdown("---") 
    if user_query := st.chat_input("Ask about your document..."):
        
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        
        with st.chat_message("assistant"):
            if not os.environ.get("GROQ_API_KEY"):
                st.error("Please enter API Key in sidebar.")
            else:
                with st.spinner("Thinking..."):
                    response = ask_document(st.session_state.doc_text, user_query)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})