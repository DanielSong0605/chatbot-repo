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
import time
import random

# Loads in the API key kept in a .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize Groq client
client = Groq(api_key=api_key)

# Create an event to be able to stop speech playback
stop_speech_event = threading.Event()

with open("meta_info.json", "r") as f:
    meta_info = json.load(f)

# Function to speak text using gTTS
def speak(text):
    # Creates a temporary file to store the TTS audio
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.write_to_fp(tmpfile)
        temp_path = tmpfile.name

    sound = pygame.mixer.Sound(temp_path)
    channel = sound.play()

    # Continue playing until finished or stop_speech_event is set
    while channel.get_busy() and not stop_speech_event.is_set():
        pygame.time.wait(100)

    channel.stop()

# Lists all available microphones
def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()

    for index, mic_name in enumerate(mic_list):
        print(f"Microphone {index}: {mic_name}")

# Listens for user voice input
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
def think(conversation, tasks):
    # Creates a summarizing agent that summarizes the conversation history to find the user's question
    summarizing_agent_memory = [{"role": "system", "content": "Here is the conversation history:\n\n" + '\n'.join([f"{msg["role"].title()}: {msg["content"]}" for msg in conversation[1:]])}]
    summarizing_agent = ModelWrapper(memory=summarizing_agent_memory)
    summarizing_agent_prompt = ''.join(meta_info["summarizing_agent"]["prompt"])
    question = summarizing_agent.call_model(summarizing_agent_prompt, prompt_role="system")

    # Creates a thinking agent that processes the question and generates an answer
    thinking_agent_prompt = ''.join(meta_info["thinking_agent"]["prompt"]) + question
    thinking_agent = ModelWrapper()
    answer = thinking_agent.call_model(thinking_agent_prompt, prompt_role="system")

    # Creates a naming agent that generates a concise name for the question to create a file name
    naming_agent_prompt = ''.join(meta_info["naming_agent"]["prompt"]) + f"\nThe name should not be creative - only informative, like the title to a study rather than a book. Generate a short, concise, informative name for the following question (~2-3 words), separating words using spaces, based off this question: {question}"
    naming_agent = ModelWrapper()
    name = naming_agent.call_model(naming_agent_prompt, prompt_role="system")
    file_name = os.path.join('agent_answers', ''.join([c for c in name.lower().strip().replace(" ", "_") if c.isalnum() or c == "_"]) + f"{str(random.randint(1000, 9999))}.txt")

    # Stores the question and answer in a text file to be viewed by the user
    with open(file_name, "w") as f:
        f.write(f"Question: {question}\n\nAnswer: {answer}")
    
    print(f"\n\nQuestion answered! File saved as: {file_name}\n\n")

    # Adds the question to the completed tasks list to give the main agent knowledge of the completed task
    tasks.append((question, False))

# Main interaction loop
def main():
    # Creates an empty list to store future completed tasks
    completed_tasks = []

    # Loads the base model information from the meta_info.json file
    base_model_info = meta_info["base_agent"]
    agent_name = base_model_info["name"].lower()
    break_word = "quit"

    sys_prompt = ''.join(base_model_info["prompt"])

    # Allows the user to decide on the input and output methods of the agent (voice or text)
    use_voice_input = input("Do you want to use voice input? (y/n): ").strip().lower() == "y"
    use_voice_output = input("Do you want to use voice output? (y/n): ").strip().lower() == "y"

    # Lists the available microphones if voice input is selected
    if use_voice_input:
        print("Available microphones:")
        list_microphones()
        mic_index = int(input("Enter the microphone index you want to use: "))

    agent = ModelWrapper(sys_prompt=sys_prompt)
    running = True

    while running:
        # Gets user input through voice or text
        if use_voice_input:
            user_prompt = listen_with_specific_microphone(mic_index)

            # Stops the speech playback if the user has spoken
            if user_prompt != "":
                stop_speech_event.set()
        else:
            user_prompt = input("User: ")

            # Stops the speech playback if the user has typed something
            stop_speech_event.set()

        if break_word in user_prompt.lower():
            running = False
        elif agent_name in user_prompt.lower():
            # Loops through all the completed tasks and adds them to the agent's memory
            for i in range(len(completed_tasks)):
                task, seen = completed_tasks[i]
                agent.memory.append({"role": "system", "content": f"User question asking '{task}' has been completed and stored."})

                completed_tasks[i] = (task, True)

            # Removes all tasks that have been seen by the agent
            completed_tasks[:] = [(task, False) for task, seen in completed_tasks if not seen]

            print(agent_name.title() + " is pondering...")
            response = agent.call_model(user_prompt)

            # If the response contains the think() method, it will start a new thread to process the question
            if "{think()}" in response:
                response = response.replace("{think()}", "").strip()
                agent.memory.append({"role": "system", "content": "User question is currently being processed using the think() method."})
                threading.Thread(target=think, daemon=True, args=(agent.memory, completed_tasks)).start()

            print(f"{agent_name.title()}: {response}")

            # If voice output is selected, it will clear the speech event and speak the response
            if use_voice_output:
                stop_speech_event.clear()
                threading.Thread(target=speak, daemon=True, args=(response,)).start()


if __name__ == "__main__":
    main()
