# app.py

import streamlit as st
from chatbot import get_streaming_response

# ---------------- SETUP ----------------
st.set_page_config(
    page_title="English Tutor AI",
    page_icon="📚",
    layout="centered"
)

# ---------------- HEADER ----------------
st.markdown("# 📚 English Tutor AI")
st.markdown("### ✨ Learn English with your personal AI teacher")
st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    tone = st.selectbox(
        "Choose Teaching Style",
        ["Friendly 😊", "Strict 🧑‍🏫", "Motivational 💪"]
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are a {tone} English teacher. Help improve grammar, vocabulary and sentence formation."
        }
    ]

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("💬 Type your message here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- STREAM RESPONSE ----------------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in get_streaming_response(st.session_state.messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption("🚀 Built with Streamlit | Practice daily to improve your English")