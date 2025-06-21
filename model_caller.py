from groq import Groq, APIStatusError, RateLimitError
import os
from dotenv import load_dotenv

load_dotenv()

i = 1
clients = []
while f"GROQ_API_KEY_{i}" in os.environ:
    clients.append(Groq(api_key=os.getenv(f"GROQ_API_KEY_{i}")))
    i += 1

models = ["meta-llama/llama-4-maverick-17b-128e-instruct", "llama3-70b-8192", "meta-llama/llama-4-scout-17b-16e-instruct"]

def call_model(messages, target_model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=2048, verbose=False):
    completion = None
    available_models = models.copy()

    if target_model in available_models:
        available_models.remove(target_model)

    available_models.insert(0, target_model)
        
    for model in models:
        for client in clients:
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
        
        if verbose:
            print("Warning: No API keys successful. Retrying with a different model.")
            

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response
