# chatbot.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = OpenAI(
    base_url="http://localhost:11434/v1" ,
    api_key="ollama"
)

def get_streaming_response(messages, model="phi3.5"):
    """
    Generator function to stream response from LLM
    """
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content