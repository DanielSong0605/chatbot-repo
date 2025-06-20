import speech_recognition as sr
from gtts import gTTS
import io
import pygame
from groq import Groq
import os
import json
from dotenv import load_dotenv
from model_wrapper import ModelWrapper
import threading
import tempfile

# Loads in the API key kept in a .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize Groq client
client = Groq(api_key=api_key)

stop_speech_event = threading.Event()

with open("meta_info.json", "r") as f:
    meta_info = json.load(f)

# Function to speak text using gTTS
def speak(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.write_to_fp(tmpfile)
        temp_path = tmpfile.name

    sound = pygame.mixer.Sound(temp_path)
    channel = sound.play()

    while channel.get_busy() and not stop_speech_event.is_set():
        pygame.time.wait(100)

    channel.stop()

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

# Function that allows the agent to think for longer
def think(conversation):
    summarizing_agent_memory = [{"role": "system", "content": "Here is the conversation history:\n\n" + '\n'.join([f"{msg["role"].title()}: {msg["content"]}" for msg in conversation[1:]])}]
    # print(summarizing_agent_memory)
    summarizing_agent = ModelWrapper(memory=summarizing_agent_memory)
    summarizing_agent_prompt = ''.join(meta_info["summarizing_agent"]["prompt"])
    question = summarizing_agent.call_model(summarizing_agent_prompt, prompt_role="system")
    print(f"\n\nQuestion identified: {question}\n\n")

    thinking_agent_prompt = ''.join(meta_info["thinking_agent"]["prompt"]) + question
    thinking_agent = ModelWrapper()
    answer = thinking_agent.call_model(thinking_agent_prompt, prompt_role="system")
    print(f"\n\nQuestion answered:\n{answer}\n\n")

# Main interaction loop
def main():
    base_model_info = meta_info["base_agent"]
    agent_name = base_model_info["name"].lower()
    break_word = "quit"

    sys_prompt = ''.join(base_model_info["prompt"])

    # Allows the user to decide on the input and output methods of the agent
    use_voice_input = input("Do you want to use voice input? (y/n): ").strip().lower() == "y"
    use_voice_output = input("Do you want to use voice output? (y/n): ").strip().lower() == "y"

    if use_voice_input:
        print("Available microphones:")
        list_microphones()
        mic_index = int(input("Enter the microphone index you want to use: "))

    agent = ModelWrapper(sys_prompt=sys_prompt)
    running = True

    while running:
        if use_voice_input:
            user_prompt = listen_with_specific_microphone(mic_index)
            if user_prompt != "":
                stop_speech_event.set()
        else:
            user_prompt = input("User: ")
            stop_speech_event.set()

        if break_word in user_prompt.lower():
            running = False
        elif agent_name in user_prompt.lower():
            print(agent_name.title() + " is pondering...")
            response = agent.call_model(user_prompt)

            if "{think()}" in response:
                print("Thinking...", response)
                response = response.replace("{think()}", "").strip()
                think(agent.memory)
                # threading.Thread(target=speak, daemon=True, args=(response,)).start()

            print(f"{agent_name.title()}: {response}")

            if use_voice_output:
                stop_speech_event.clear()
                threading.Thread(target=speak, daemon=True, args=(response,)).start()


if __name__ == "__main__":
    main()
