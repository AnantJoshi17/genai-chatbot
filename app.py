import os

import streamlit as st
from groq import Groq

st.set_page_config(page_title="GenAI Chatbot", page_icon="🤖")

MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]


def get_api_key():
    """Look for the Groq key in Streamlit secrets, then env vars, then the sidebar."""
    try:
        if st.secrets.get("GROQ_API_KEY"):
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass  # no secrets.toml file
    return os.getenv("GROQ_API_KEY", "")


# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = get_api_key() or st.text_input("Groq API key", type="password")
    model = st.selectbox("Model", MODELS)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    system_prompt = st.text_area(
        "System prompt", "You are a helpful, friendly assistant. Keep answers clear and concise."
    )
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- Main ----------
st.title("🤖 GenAI Chatbot")
st.caption("Powered by Groq LLMs + Streamlit")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    if not api_key:
        st.warning("Please add your Groq API key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=api_key)
    history = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model, messages=history, temperature=temperature, stream=True
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )
        except Exception as e:
            reply = f"⚠️ Error: {e}"
            st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
