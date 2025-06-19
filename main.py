import speech_recognition as sr
from gtts import gTTS
import io
import pygame
from groq import Groq
import os
import json
from dotenv import load_dotenv
from model_wrapper import ModelWrapper

# Loads in the API key kept in a .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize Groq client
client = Groq(api_key=api_key)

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

# Lists all available microphones
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

# Main interaction loop
def main():
    with open("meta_info.json", "r") as f:
        meta_info = json.load(f)

    agent_name = meta_info["agent_name"].lower()
    break_word = "giggity goo"

    sys_prompt = meta_info["prompt"]

    print("Available microphones:")
    list_microphones()
    mic_index = int(input("Enter the microphone index you want to use: "))

    agent = ModelWrapper(sys_prompt=sys_prompt)
    running = True

    while running:
        user_prompt = listen_with_specific_microphone(mic_index)

        if break_word in user_prompt:
            running = False

        if agent_name in user_prompt:
            print(agent_name.title() + " is pondering...") 
            response = agent.call_model(user_prompt)
            print(f"{agent_name.title()}: {response}")
            speak(response)


if __name__ == "__main__":
    main()
