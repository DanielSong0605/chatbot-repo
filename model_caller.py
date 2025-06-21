from groq import Groq, APIStatusError, RateLimitError
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

backup_client = Groq(
    api_key=os.getenv("GROQ_API_KEY_2")
)

def call_model(messages, model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=2048, verbose=False):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=True,
            stop=None,
        )
    except (APIStatusError, RateLimitError) as e:
        if verbose:
            print("Warning: APIStatusError or RateLimitError encountered. Retrying with a different API key.")

        try:
            completion = backup_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=1,
                max_completion_tokens=max_tokens,
                top_p=1,
                stream=True,
                stop=None,
            )
        except (APIStatusError, RateLimitError) as e:
            if verbose:
                print("Warning: APIStatusError or RateLimitError encountered. Retrying with a different model.")

            completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=1,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=True,
            stop=None,
            )
            

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response
