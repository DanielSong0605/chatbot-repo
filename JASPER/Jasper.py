import speech_recognition as sr
from gtts import gTTS
import io
import pygame
from groq import Groq
import os
import json


# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize Groq client
client = Groq(api_key="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")  

# File to store conversation memory
memory_file = "memory.json"

# Load memory from file if it exists
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            return json.load(f)
    return []

# Save memory to file
def save_memory(memory):
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=2)

# Add new exchange to memory
def add_to_memory(memory, user_input, ai_response):
    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": ai_response})
    save_memory(memory)

# Function to speak text using gTTS
def speak(text):
    tts = gTTS(text=text, lang="en")
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    pygame.mixer.music.load(audio_stream, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# List available microphones
def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    for index, mic_name in enumerate(mic_list):
        print(f"Microphone {index}: {mic_name}")

# Listen for user voice input
def listen_with_specific_microphone(mic_index):
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=mic_index) as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service error.")
        return ""

# Ask AI using Groq
def ask_ai_streaming(prompt, chat_history):
    full_response = ""
    new_chat_history = chat_history.copy()
    new_chat_history.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=new_chat_history,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True
    )

    for chunk in completion:
        content_piece = chunk.choices[0].delta.content or ""
        print(content_piece, end="", flush=True)
        full_response += content_piece
    new_chat_history.append({"role": "assistant", "content": full_response})
    print("\n")
    return full_response, new_chat_history

# Main interaction loop
def main():
    chat_history = []
    bot_name = "aria"2
    with open("background.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.replace("{bot_name}", bot_name)
    print(prompt)
    chat_history.append({"role": "system", "content": prompt})
    print("Available microphones:")
    list_microphones()
    mic_index = int(input("Enter the microphone index you want to use: "))

    memory = load_memory()
    while True:
        command = listen_with_specific_microphone(mic_index)
        if bot_name in command:
            print(bot_name.title() + " is pondering...") 

            if "giggity goo" in command:
                break
            else:
                response, chat_history = ask_ai_streaming(command, chat_history)
            speak(response)    
        if "giggity goo" in command:
                break
            
           

if __name__ == "__main__":
    main()
