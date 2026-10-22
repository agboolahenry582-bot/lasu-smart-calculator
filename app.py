import streamlit as st
import os, requests, urllib.parse
from groq import Groq
import fitz, docx

st.set_page_config(page_title="HENRY TIMS AI", page_icon="🤖", layout="wide")
st.markdown('<h1 style="text-align:center;background: linear-gradient(90deg, #00f5ff, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🤖 HENRY TIMS AI</h1><p style="text-align:center">Built by Henry Agboola</p>', unsafe_allow_html=True)

GROQ_KEY = None
try:
    GROQ_KEY = st.secrets.get("GROQ_API_KEY")
except:
    pass
if not GROQ_KEY:
    GROQ_KEY = os.getenv("GROQ_API_KEY")
if GROQ_KEY:
    st.sidebar.success("Key found")
else:
    GROQ_KEY = st.sidebar.text_input("Groq Key:", type="password")

client = None
if GROQ_KEY and GROQ_KEY.startswith("gsk_") and len(GROQ_KEY) > 20:
    try:
        client = Groq(api_key=GROQ_KEY)
    except Exception as e:
        st.sidebar.error(f"Key error: {e}")

if "history" not in st.session_state:
    st.session_state.history = []

tab_chat, tab_img = st.tabs(["💬 CHAT", "🎨 IMAGE CAT"])

with tab_chat:
    for m in st.session_state.history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input("Ask HENRY..."):
        st.session_state.history.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        if not client:
            with st.chat_message("assistant"): st.error("Add REAL Groq key in Secrets! Get at console.groq.com/keys - not gsk_... placeholder")
        else:
            with st.chat_message("assistant"):
                try:
                    # Try best model
                    stream = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"system","content":"You are HENRY TIMS AI by Henry Agboola"}]+st.session_state.history, stream=True)
                    out=""; box=st.empty()
                    for ch in stream:
                        if ch.choices[0].delta.content:
                            out+=ch.choices[0].delta.content; box.markdown(out)
                    box.markdown(out)
                    st.session_state.history.append({"role":"assistant","content":out})
                except Exception as e:
                    st.error(f"Groq Error: {e}")
                    st.info("Fix: Go to Manage App > Settings > Secrets > Delete old key > Add REAL key from console.groq.com/keys > Save > Reboot")

with tab_img:
    ip = st.text_input("Cat prompt", "a cute orange tabby cat on Dell laptop keyboard")
    if st.button("Generate Cat"):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(ip)}?width=1024&height=1024&nologo=true"
        st.image(url, caption=ip)
        st.markdown(f"[Open Image]({url})")

st.caption("© HENRY TIMS AI - Henry Agboola")
