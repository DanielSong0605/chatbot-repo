from groq import Groq, APIStatusError
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def call_model(messages, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
    except APIStatusError as e:
        print("Warning: APIStatusError encountered. Retrying with a different model.")

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            stream=True,
            stop=None,
        )

    assistant_message = ""
    for chunk in completion:
        assistant_message += chunk.choices[0].delta.content or ""

    return assistant_message
