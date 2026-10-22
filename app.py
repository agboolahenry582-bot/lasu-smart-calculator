import streamlit as st
import os, requests, urllib.parse
from groq import Groq
import fitz, docx, pandas as pd

st.set_page_config(page_title="HENRY TIMS AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at 20% 30%, #0f0c29 0%, #302b63 50%, #24243e 100%); color:white; }
.hero h1 { font-size: 3.2rem; background: linear-gradient(90deg, #00f5ff, #ff00ff, #ffcc00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-weight:900; }
</style>
""", unsafe_allow_html=True)

# --- KEY FIX: READ FROM SECRETS + ENV + SIDEBAR ---
GROQ_KEY = None
try:
    GROQ_KEY = st.secrets.get("GROQ_API_KEY")
except:
    pass
if not GROQ_KEY:
    GROQ_KEY = os.getenv("GROQ_API_KEY")

if GROQ_KEY:
    st.sidebar.success("🤖 HENRY TIMS AI Cloud Mode ON")
else:
    GROQ_KEY = st.sidebar.text_input("⚡ Add Groq Key (get free at console.groq.com/keys):", type="password")

client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

if "history" not in st.session_state:
    st.session_state.history = [{"role":"system","content": "You are HENRY TIMS AI, an unlimited AI assistant built by Henry Agboola. You are helpful, smart, fast like Gemini Ultra. You can answer anything, explain nouns, generate images via description, etc."}]

st.sidebar.header("📁 Upload Files for HENRY")
uploaded = st.sidebar.file_uploader("PDF, DOCX, TXT, CSV", type=["pdf","docx","txt","csv"], accept_multiple_files=True)
file_ctx = ""
if uploaded:
    for f in uploaded:
        try:
            if f.name.endswith(".pdf"):
                doc = fitz.open(stream=f.read(), filetype="pdf")
                file_ctx += "".join([p.get_text() for p in doc])[:4000]
            elif f.name.endswith(".docx"):
                d=docx.Document(f)
                file_ctx += "\n".join([p.text for p in d.paragraphs])[:4000]
            else:
                file_ctx += f.read().decode(errors="ignore")[:4000]
        except:
            pass

st.markdown('<div class="hero"><h1>🤖 HENRY TIMS AI</h1><p style="text-align:center;color:#cbd5e0;">Unlimited • Fast • Your Personal Gemini • Built by Henry Agboola</p></div>', unsafe_allow_html=True)

tab_chat, tab_search, tab_image = st.tabs(["💬 CHAT", "🔍 WHAT IS A NOUN / GOOGLE", "🎨 IMAGE GEN (CAT)"])

with tab_chat:
    for m in st.session_state.history[1:]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Ask HENRY TIMS AI anything..."):
        full_prompt = f"FILES CONTEXT: {file_ctx}\n\nUSER QUESTION: {prompt}" if file_ctx else prompt
        st.session_state.history.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        if not client:
            with st.chat_message("assistant"):
                st.error("⚠️ Add GROQ_API_KEY in Streamlit Cloud Secrets! Go to Manage App > Settings > Secrets")
                st.code('GROQ_API_KEY = "gsk_..."')
        else:
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(model="llama-3.1-8b-instant", messages=st.session_state.history[:-1]+[{"role":"user","content":full_prompt}], stream=True)
                out=""; box=st.empty()
                for ch in stream:
                    if ch.choices[0].delta.content:
                        out+=ch.choices[0].delta.content
                        box.markdown(out+"▌")
                box.markdown(out)
                st.session_state.history.append({"role":"assistant","content":out})

with tab_search:
    st.subheader("🔍 Ask what is a noun - HENRY will search web")
    q = st.text_input("Search query", value="what is a noun", key="search_q")
    if st.button("Search & Answer"):
        if not client:
            st.error("Add Groq Key first")
        else:
            with st.spinner("HENRY searching web..."):
                web_context = ""
                # Try DuckDuckGo + Wikipedia for noun
                try:
                    # Wikipedia for noun
                    wiki = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}", timeout=5).json()
                    web_context += wiki.get("extract","")[:2000]
                except:
                    pass
                try:
                    ddg = requests.get(f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json", timeout=5).json()
                    web_context += str(ddg.get("AbstractText",""))[:2000]
                except:
                    pass
                
                prompt = f"User searched: '{q}'. Web context: {web_context}. Answer like Gemini, explain clearly, examples. If noun, define types etc."
                res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}])
                st.success(res.choices[0].message.content)

with tab_image:
    st.subheader("🎨 HENRY Image Generator - Try 'i need a cat'")
    ip = st.text_input("Describe image", value="i need a cat not working for anything - a cute fluffy cat", key="img_q")
    if st.button("Generate Image NOW"):
        if ip:
            # 100% Working Pollinations URL
            encoded = urllib.parse.quote_plus(ip)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true&enhance=true"
            st.image(img_url, caption=f"HENRY Generated: {ip}", use_column_width=True)
            st.markdown(f"**Direct Link:** {img_url}")
            st.balloons()
            st.info("Image generated by HENRY TIMS AI via Pollinations Flux - Fast & Free")

st.divider()
st.caption("© 2026 HENRY TIMS AI | Built with ❤️ by Henry Agboola | agboolahenry582-bot | Public AI for Everyone")
