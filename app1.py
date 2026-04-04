import streamlit as st
from chatbot import get_streaming_response
import uuid
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
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
    st.session_state.chats[chat_id] = []

if "mode" not in st.session_state:
    st.session_state.mode = "General Chat"

if "pending_mode" not in st.session_state:
    st.session_state.pending_mode = None

if st.session_state.pending_mode:
    st.session_state.mode = st.session_state.pending_mode
    st.session_state.pending_mode = None

# QUIZ STATE
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

# ✅ NEW: FINAL RESULT STORAGE (FIX)
if "final_score" not in st.session_state:
    st.session_state.final_score = 0

if "final_total" not in st.session_state:
    st.session_state.final_total = 0

if "final_accuracy" not in st.session_state:
    st.session_state.final_accuracy = 0

# ---------------- PDF FUNCTION ----------------
def generate_pdf(chat_history):
    doc = SimpleDocTemplate("quiz_history.pdf")
    styles = getSampleStyleSheet()
    content = []

    # ✅ ADD RESULT INTO PDF
    content.append(Paragraph("📊 Quiz Result", styles["Heading2"]))
    content.append(Paragraph(f"Score: {st.session_state.final_score}/{st.session_state.final_total}", styles["Normal"]))
    content.append(Paragraph(f"Accuracy: {st.session_state.final_accuracy}%", styles["Normal"]))
    content.append(Paragraph(" ", styles["Normal"]))

    # CHAT HISTORY
    for msg in chat_history:
        if msg["role"] != "system":
            text = f"{msg['role'].upper()}: {msg['content']}"
            content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)
    return "quiz_history.pdf"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("💬 Chats")

    if st.button("➕ New Chat"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = []
        st.rerun()

    st.divider()

    for chat_id in st.session_state.chats.keys():
        if st.button(f"Chat {chat_id[:6]}", key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.divider()

    st.header("🎯 Learning Mode")
    st.radio(
        "Choose Mode:",
        ["General Chat", "Grammar Correction", "Vocabulary", "Practice Quiz"],
        key="mode"
    )

    st.divider()

    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("# 📚 English Tutor AI")
st.markdown("### ✨ Learn English with your personal AI teacher")

st.info(f"🎯 Current Mode: {st.session_state.mode}")

# ---------------- QUICK BUTTONS ----------------
col1, col2, col3 = st.columns(3)

if col1.button("✍️ Fix My Sentence", use_container_width=True):
    st.session_state.pending_mode = "Grammar Correction"
    st.rerun()

if col2.button("📖 Learn Words", use_container_width=True):
    st.session_state.pending_mode = "Vocabulary"
    st.rerun()

if col3.button("🧪 Take Quiz", use_container_width=True):
    st.session_state.pending_mode = "Practice Quiz"
    st.rerun()

st.divider()

# ---------------- CURRENT CHAT ----------------
messages = st.session_state.chats[st.session_state.current_chat]

# ---------------- SHOW CHAT ----------------
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- RESULT UI ----------------
if st.session_state.show_result:
    total = st.session_state.total_questions
    score = st.session_state.score
    accuracy = int((score / total) * 100) if total > 0 else 0

    # ✅ STORE FINAL RESULT (FIX)
    st.session_state.final_score = score
    st.session_state.final_total = total
    st.session_state.final_accuracy = accuracy

    if accuracy >= 80:
        level = "🟢 Easy"
    elif accuracy >= 50:
        level = "🟡 Medium"
    else:
        level = "🔴 Hard"

    st.markdown("## 📊 Your Quiz Result")

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Score", f"{score}/{total}")
    col2.metric("📈 Accuracy", f"{accuracy}%")
    col3.metric("🎯 Level", level)

    st.progress(accuracy / 100)
    st.success("Great effort! Keep practicing 🚀")

    # ❌ REMOVED RESET HERE (IMPORTANT FIX)
    st.session_state.show_result = False

# ---------------- MODE LOGIC ----------------
def build_prompt(user_input):
    mode = st.session_state.mode

    if mode == "Grammar Correction":
        return f"Correct this sentence and explain simply:\n{user_input}"

    elif mode == "Vocabulary":
        return f"Teach vocabulary with meanings and examples:\n{user_input}"

    elif mode == "Practice Quiz":

        user_input_clean = user_input.strip().lower()

        if user_input_clean == "exit":
            st.session_state.quiz_active = False
            st.session_state.show_result = True
            return "📊 Generating result..."

        if user_input_clean == "start":
            st.session_state.quiz_active = True
            st.session_state.score = 0
            st.session_state.total_questions = 0

            return """
You are an English quiz generator.

STRICT RULES:
- Only grammar/vocabulary questions
- No general knowledge
- No explanation

FORMAT:

Question: ...
A) ...
B) ...
C) ...
D) ...

Correct Answer: X

What is your answer?
"""

        if (
            st.session_state.quiz_active
            and st.session_state.correct_answer is not None
            and user_input.strip().upper() in ["A", "B", "C", "D"]
        ):

            user_ans = user_input.strip().upper()
            correct_ans = st.session_state.correct_answer

            st.session_state.total_questions += 1

            if user_ans == correct_ans:
                st.session_state.score += 1
                result = "Correct"
            else:
                result = "Wrong"

            return f"""
You are an English tutor.

STRICT RULES:
- DO NOT change format
- DO NOT add extra text
- DO NOT skip sections
- ALWAYS follow exact structure

FORMAT:

You selected answer: {user_ans}
Correct answer is: {correct_ans}

Result: {result}

Explanation:
Explain in 2-3 simple lines why the correct answer is correct.

Next Question:
Choose a grammar or vocabulary question.

A) ...
B) ...
C) ...
D) ...

Correct Answer: X

What is your answer?
"""

        if not st.session_state.quiz_active:
            return "👉 Type 'start' to begin quiz."

        return user_input

    return user_input

# ---------------- INPUT ----------------
prompt = st.chat_input("💬 Type your message here...")

# ---------------- PROCESS ----------------
if prompt:
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    final_prompt = build_prompt(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        temp_messages = messages.copy()
        temp_messages[-1] = {"role": "user", "content": final_prompt}

        for chunk in get_streaming_response(temp_messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        match = re.search(r"Correct Answer:\s*([A-D])", full_response)
        if match:
            st.session_state.correct_answer = match.group(1)
            full_response = re.sub(r"Correct Answer:\s*[A-D]", "", full_response)

        message_placeholder.markdown(full_response)

    messages.append({"role": "assistant", "content": full_response})

# ---------------- PDF ----------------
if st.session_state.mode == "Practice Quiz" and messages:
    if st.button("📄 Download Quiz History as PDF"):

        file_path = generate_pdf(messages)

        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="quiz_history.pdf",
                mime="application/pdf"
            )

        # ✅ RESET ONLY AFTER DOWNLOAD
        st.session_state.score = 0
        st.session_state.total_questions = 0

# ---------------- FOOTER ----------------
st.divider()
st.caption("🚀 Built with Streamlit | Practice daily to improve your English")