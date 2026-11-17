# 🤖 GenAI Chatbot (Groq + Streamlit)

A simple end-to-end chatbot that uses Groq-hosted open LLMs (GPT-OSS, Qwen) with a Streamlit chat UI.

## Features
- ChatGPT-style chat interface with streaming replies
- Remembers the conversation during a session
- Choose the model, temperature and system prompt from the sidebar
- Clear-chat button

## Tech stack
| Part | Tool |
|------|------|
| LLM  | Groq API (GPT-OSS 120B / 20B, Qwen 3.8 27B) |
| UI   | Streamlit |
| Language | Python |

## How it works
1. The user types a message in the chat box.
2. The app adds it to the chat history stored in `st.session_state`.
3. The system prompt plus the full history go to the Groq chat completions API.
4. The reply streams back token by token and is saved to the history.

## Run locally
```bash
pip install -r requirements.txt
```
Paste your key into `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_..."
```
Then start the app:
```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (free)
1. Push this folder to a GitHub repo. `secrets.toml` is git-ignored, so your key stays private.
2. Go to https://share.streamlit.io, click **Create app**, and pick your repo with `app.py` as the main file.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
4. Click **Deploy**. You get a public URL.
