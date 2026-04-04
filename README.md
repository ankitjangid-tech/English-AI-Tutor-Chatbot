# 📚 English Tutor AI Chatbot

[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://ankit-english-ai-tutor-chatbot.streamlit.app/)  
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

✨ Learn English with your **personal AI tutor**! Practice grammar, vocabulary, and take interactive quizzes—all in one chatbot interface.

---

## 🌐 Live Demo

Try it live here: [English Tutor AI](https://ankit-english-ai-tutor-chatbot.streamlit.app/)  

![Demo Screenshot](https://via.placeholder.com/800x400.png?text=English+Tutor+AI+Demo)  
*Replace the above with a real screenshot or GIF of your app in action*

---

## 🚀 Features

- 💬 **Interactive Chat**: Talk to your AI English tutor just like a real teacher.
- ✍️ **Grammar Correction**: Fix your sentences and learn why.
- 📖 **Vocabulary Builder**: Learn new words with meanings and examples.
- 🧪 **Practice Quiz**: Test your grammar and vocabulary with instant feedback.
- 📄 **Download Quiz History**: Save your quiz results and chat as a PDF.
- 🆕 **Multi-Chat Support**: Start multiple chats and switch between them easily.
- 🎯 **Learning Modes**: Switch between general chat, grammar, vocabulary, or quizzes.

---

## ⚡ How It Works

1. **Start a new chat** using the sidebar.  
2. **Choose a mode**: General Chat, Grammar Correction, Vocabulary, or Practice Quiz.  
3. **Type your message** in the chat input. The AI will respond interactively.  
4. **Quiz mode**: Type `start` to begin the quiz and select answers (A/B/C/D).  
5. **Download your progress** as a PDF for review.

---

## 🛠 Built With

- [Streamlit](https://streamlit.io/) – For building the interactive web app.  
- [Python](https://www.python.org/) – Core programming language.  
- [ReportLab](https://www.reportlab.com/) – Generate downloadable PDF quiz history.  
- OpenAI GPT-3.5 (via `chatbot.py`) – AI backend for conversation, grammar, and quizzes.

---

## 📂 Installation (Local)

```bash
# Clone the repository
git clone https://github.com/yourusername/english-ai-tutor-chatbot.git
cd english-ai-tutor-chatbot

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app1.py
