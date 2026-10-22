import streamlit as st

st.set_page_config(page_title="LASU AI SuperApp", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
h1 { color: white; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 LASU AI SuperApp")
st.write("Welcome! This AI can do anything + search Google + generate images")

# Sidebar
st.sidebar.title("Features")
mode = st.sidebar.selectbox("Choose Mode", ["Smart Calculator", "AI Chat (Groq)", "Google Search", "Image Generator"])

if mode == "Smart Calculator":
    st.subheader("🧮 LASU Smart Calculator")
    expr = st.text_input("Enter calculation (e.g. 5*5 + GPA 3.5*20):", "2+2")
    if st.button("Calculate"):
        try:
            result = eval(expr)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif mode == "AI Chat (Groq)":
    st.subheader("🤖 Chat with AI")
    st.info("Add your GROQ_API_KEY to .env to make this work")
    prompt = st.text_area("Ask anything:")
    if st.button("Ask AI"):
        st.write("AI Response will appear here after you add Groq key.")

elif mode == "Google Search":
    st.subheader("🔍 Google Search")
    query = st.text_input("Search Google:")
    if st.button("Search"):
        st.write(f"Searching for: {query} (add googlesearch-python logic)")

elif mode == "Image Generator":
    st.subheader("🎨 Image Generator")
    img_prompt = st.text_input("Describe image:")
    if st.button("Generate"):
        st.write(f"Generating image for: {img_prompt}")

st.markdown("---")
st.caption("Built for LASU - by you!")
