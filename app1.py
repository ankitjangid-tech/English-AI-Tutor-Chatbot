import streamlit as st
from chatbot import get_streaming_response
import uuid

# ---------------- SETUP ----------------
st.set_page_config(
    page_title="English Tutor AI",
    page_icon="📚",
    layout="centered"
)

# ---------------- SESSION INIT ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = [
        {
            "role": "system",
            "content": "You are a friendly English teacher. Help improve grammar, vocabulary and sentence formation."
        }
    ]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("💬 Chats")

    # ➕ New Chat
    if st.button("➕ New Chat"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = [
            {
                "role": "system",
                "content": "You are a friendly English teacher."
            }
        ]
        st.rerun()

    st.divider()

    # 📜 Chat History List
    for chat_id in st.session_state.chats.keys():
        if st.button(f"Chat {chat_id[:6]}", key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.divider()

    # ⚙️ Settings
    st.header("⚙️ Settings")
    tone = st.selectbox(
        "Choose Teaching Style",
        ["Friendly 😊", "Strict 🧑‍🏫", "Motivational 💪"]
    )

    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("# 📚 English Tutor AI")
st.markdown("### ✨ Learn English with your personal AI teacher")
st.divider()

# ---------------- CURRENT CHAT ----------------
messages = st.session_state.chats[st.session_state.current_chat]

# ---------------- SHOW CHAT ----------------
for msg in messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("💬 Type your message here...")

if prompt:
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- STREAM RESPONSE ----------------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in get_streaming_response(messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    messages.append({"role": "assistant", "content": full_response})

# ---------------- FOOTER ----------------
st.divider()
st.caption("🚀 Built with Streamlit | Practice daily to improve your English")