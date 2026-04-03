# chatbot.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")

if api_key:
    print(api_key[:8]) 
else: 
    print("api not found")

# Initialize client
client=OpenAI(api_key=api_key)

def get_streaming_response(messages, model="gpt-4o-mini"):
    """
    Generator function to stream response from LLM
    """
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=150,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content