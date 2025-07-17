import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import json
from model_wrapper import ModelWrapper
import threading
import tempfile
import random
import time
from tools import all_tools
from datetime import datetime
from langchain.globals import set_verbose
from dotenv import load_dotenv
# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Sets lanchain verbose variable to true to print important chain events
set_verbose(True)

# Create an event to be able to stop speech playback
stop_speech_event = threading.Event()

# Creates a variable for the filepath where the chat history will be logged
chat_log_file_path = "chat_log.json"

# Creates a list of words that will activate the code that checks if the agent should sleep to avoid unnecessary checks
sleep_trigger_words = ["bed", "bye", "deactivate", "dormancy", "exit", "goodnight", "nap", "offline", "pause", "power", "quit", "shut", "sleep", "sleepy", "stop", "turn"]

# Load in the meta info to be used later
with open("meta_info.json", "r") as f:
    meta_info = json.load(f)

# Creates an empty json file to store conversation history if necessary
if not os.path.exists(chat_log_file_path):
    with open(chat_log_file_path, "w") as f:
        json.dump({}, f, indent=4)

# Function to speak text using gTTS
def speak(text):
    # Creates a temporary file to store the TTS audio
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.write_to_fp(tmpfile)
        temp_path = tmpfile.name

    # Playes the audio file
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

# Process a single section of the plan to recombine them later
def process_section(section, full_plan, question, section_index, finished_sections):
    thinking_prompt = ''.join(meta_info["thinking_prompt"])

    editing_agent = ModelWrapper(f"{thinking_prompt}\n\n{meta_info['editing_agent']['prompt']}\nThis is the general prompt: {question}\n\nHere is the full plan: {full_plan}\n\nHere is the section to edit. Only focus on editing and improving this one section: {section}")
    discriminator_agent = ModelWrapper(f"{thinking_prompt}\n\n{meta_info['feedback_agent']['prompt']}\nThis is the general prompt: {question}\n\nHere is the full plan: {full_plan}\n\nPlease critique the next section of the plan provided to you.")
    feedback = ""

    discriminator_satisfied = False
    while not discriminator_satisfied:
        current_section = editing_agent.call_model(feedback).content.split("</think>")[-1].strip()
        feedback = discriminator_agent.call_model(f"\n\nHere is the section to critique. If you are satisfied, end with the word GOOD on its own line:\n{current_section}", prompt_role="system").content.split("</think>")[-1].strip()

        if feedback.lower().endswith("good"):
            discriminator_satisfied = True
            print(f"\n\nSection {section_index} is complete!\n")
            finished_sections[section_index] = current_section


# Function that allows the agent to think for longer:
# Finds the user's question, generates a rough plan, provides feedback on the plan, edits it, splits it into multiple parts, and processes each part in parallel
# before recombining them and finalizing the plan
def think(conversation, tasks):
    thinking_prompt = ''.join(meta_info["thinking_prompt"])

    # Creates a question agent that summarizes the conversation history to find the user's question
    question_agent_memory = [{"role": "system", "content": "Here is the conversation history:\n\n" + '\n'.join([f"{msg["role"].title()}: {msg["content"]}" for msg in conversation[1:]])}]
    question_agent = ModelWrapper(memory=question_agent_memory)
    question_agent_prompt = ''.join(meta_info["question_agent"]["prompt"])
    question = question_agent.call_model(question_agent_prompt, prompt_role="system").content
    
    # Creates a planning agent that generates a rough plan based on the question
    planning_agent_prompt = thinking_prompt + '\n\n' + ''.join(meta_info["planning_agent"]["prompt"]) + "\nHere is your problem: " + question
    planning_agent = ModelWrapper()
    plan = planning_agent.call_model(planning_agent_prompt, prompt_role="system").content
    plan = planning_agent.call_model("Please format your plan into a detailed, in-depth step-by-step numbered list.", prompt_role="system").content.split("</think>")[-1].strip()
    # print("\n\nPlan:", plan)
    
    # Creates a feedback agent that critiques the plan
    feedback_agent_prompt = thinking_prompt + '\n\n' + ''.join(meta_info["feedback_agent"]["prompt"])
    feedback_agent = ModelWrapper()

    plan_feedback = feedback_agent.call_model(feedback_agent_prompt + "\nHere is the plan to discriminate: " + plan, prompt_role="system", store_prompt=False, store_response=False).content.split("</think>")[-1].strip()
    # print("\n\nPlan Feedback:", plan_feedback)

    # Creates an editing agent that edits the plan based on the feedback
    editing_agent = ModelWrapper(f"{thinking_prompt}\n\n{meta_info["editing_agent"]["prompt"]} Here is the plan to edit:\n{plan}\n\nHere is the feedback on the plan:\n{plan_feedback}")
    plan = editing_agent.call_model().content.split("</think>")[-1].strip()
    # print("\n\nRevised Plan:", plan)

    # Creates a splitting agent that splits the plan into multiple sections to be processed in parallel
    splitting_agent = ModelWrapper(f"{thinking_prompt}\n\n{meta_info["splitting_agent"]["prompt"]}\n\nHere is the plan to split:\n{plan}")
    split_plan = (splitting_agent.call_model().content.split("</think>")[-1].strip())
    split_plan = [section.strip() for section in split_plan.split("<new>") if section != ""]
    # print("\n\nSplit Plan:", split_plan)

    # If the split plan is empty, there has been an error so we exit the thinking process
    if len(split_plan) == 0:
        print("Warning: No tasks to complete. Exiting thinking process.")
        return
    
    # Creates a list of threads to process each section of the plan in parallel
    section_threads = []
    finished_sections = {}
    for i in range(len(split_plan)):
        section_threads.append(threading.Thread(target=process_section, args=(split_plan[i], plan, question, i, finished_sections), daemon=True))
        section_threads[-1].start()

    # Waits for all threads to finish processing their sections before continuing
    for thread in section_threads:
        thread.join()

    # Sorts the finished sections by their index to maintain the original order
    sorted_sections = dict(sorted(finished_sections.items()))
    # print(sorted_sections)

    # Combines the processed sections into a single plan
    combined_plan = "\n\n".join([section for section in sorted_sections.values()])
    finalizer_agent = ModelWrapper(f"{thinking_prompt}\n\n{meta_info['editing_agent']['prompt']}\n\nYour role is to create the final version of this plan. Combine the sections and smooth out any disjointed areas. Add information where you deem it lacking and remove unnecessary tags such as 'EDITED' or 'ENHANCED' that do not contribute to the actual plan and do not help the user understand what the plan is saying; however, do not remove any important information from the plan:\n{combined_plan}")
    final_plan = finalizer_agent.call_model().content.split("</think>")[-1].strip()

    # Creates a naming agent that generates a concise name for the question to create a file name
    naming_agent_prompt = ''.join(meta_info["naming_agent"]["prompt"]) + f"\nThe name should not be creative - only informative, like the title to a study rather than a book. Generate a short, concise, informative name for the following question (~2-3 words), separating words using spaces, based off this question: {question}"
    naming_agent = ModelWrapper()
    name = naming_agent.call_model(naming_agent_prompt, prompt_role="system").content
    file_name = os.path.join('agent_answers', ''.join([c for c in name.lower().strip().replace(" ", "_") if c.isalnum() or c == "_"]) + f"{str(random.randint(1000, 9999))}.txt")

    # Stores the question and answer in a text file to be viewed by the user
    with open(file_name, "w") as f:
        f.write(f"Question: {question}\n\nAnswer: {final_plan}")
    
    # print(f"\n\nQuestion answered! File saved as: {file_name}\n\n")

    # Adds the question to the completed tasks list to give the main agent knowledge of the completed task
    tasks.append((question, False))


def call_listening_agents(user_prompt, last_response, invoking_agent, awake_status_agent, agent_name, invoking_agent_memory_length, awake_agent_memory_length):
    # Updates the invoking agent and awake agent memory with the main agent's response
    if last_response != "":
        invoking_agent.add_memory("system", f"{agent_name.title()} said: {last_response}")
    if last_response != "":
        awake_status_agent.add_memory("system", f"{agent_name.title()} said: {last_response}")

    # Preemptively checks if the user mentioned the agent to avoid having to call a LLM
    user_mentioned_agent = agent_name.lower() in user_prompt.lower()
    # Preemptively checks if the user definitely does not want to agent to sleep to avoid having to call a LLM
    check_sleep = len([True for word in sleep_trigger_words if word in user_prompt.lower()]) > 0
    # Creates a dictionary for the threads to write their responses to
    responses = {"invoked_response": (True if user_mentioned_agent else None), "awake_response": (True if not check_sleep else None)}

    # Uses the awake agent and invoking agent (if necessary) to determine if the user is addressing the main agent or wants it to sleep
    if check_sleep:
        is_deactivated_thread = threading.Thread(target=main_agent_is_deactivated, daemon=True, args=(awake_status_agent, f"User said: {user_prompt}", responses))
        is_deactivated_thread.start()

    if not user_mentioned_agent:
        is_invoked_thread = threading.Thread(target=main_agent_is_invoked, daemon=True, args=(invoking_agent, f"User said: {user_prompt}", responses))
        is_invoked_thread.start()

    if check_sleep:
        is_deactivated_thread.join()
    if not user_mentioned_agent:
       is_invoked_thread.join()

    # In case of an error, the function automatically returns default values after 5 seconds
    start_time = time.time()
    max_wait_time = 5
    while not all(val is not None for val in responses.values()):
        time.sleep(0.1)

        if time.time() - start_time >= max_wait_time:
            return False, True

    # Uses the invoking and awake agent's response to determine if the user is addressing the main agent, and/or wants the main agent to sleep
    invoking_agent_response = responses["invoked_response"]
    is_invoked = user_mentioned_agent or ''.join([c for c in invoking_agent_response.lower().split()[-1] if c.isalpha()]) == "true"

    awake_agent_response = responses["awake_response"]
    is_awake = (not check_sleep) or (not ''.join([c for c in awake_agent_response.lower().split()[-1] if c.isalpha()]) == "true")

    # Clips agent memories if too long to reduce latency
    if len(invoking_agent.memory) > invoking_agent_memory_length:
        invoking_agent.memory = [invoking_agent.memory[0]] + invoking_agent.memory[-invoking_agent_memory_length:]
    else:
         invoking_agent.memory = invoking_agent.memory[-invoking_agent_memory_length:]

    if len(awake_status_agent.memory) > awake_agent_memory_length:
        awake_status_agent.memory = [awake_status_agent.memory[0]] + awake_status_agent.memory[-awake_agent_memory_length:]
    else:
         awake_status_agent.memory = awake_status_agent.memory[-awake_agent_memory_length:]

    return is_invoked, is_awake


def main_agent_is_invoked(agent, prompt, responses):
    agent.add_memory("system", f"User message:")
    response = agent.call_model(prompt)
    responses["invoked_response"] = "result: " + response.content


def main_agent_is_deactivated(agent, prompt, responses):
    agent.add_memory("system", f"User message:")
    response = agent.call_model(prompt)
    responses["awake_response"] = "result: " + response.content


# Main interaction loop
def main():
    # Creates an ID for this specific instance of using the agent, to be used for chat history storage and other identification
    instance_id = datetime.now().strftime("%d-%m-%y %H:%M:%S") + " - " + str(random.randint(1000, 9999))

    # Creates an empty list to store future completed tasks
    completed_tasks = []

    # Loads the base model information from the meta_info.json file
    base_model_info = meta_info["base_agent"]
    agent_name = base_model_info["name"].lower()
    break_word = "quit"

    # Creates the initial 
    sys_prompt = ''.join(base_model_info["base_prompt"]) + '\n\n' + ''.join(base_model_info["thinking_prompt"])

    # Allows the user to decide on the input and output methods of the agent (voice or text)
    use_voice_input = input("Do you want to use voice input? (y/n): ").strip().lower() == "y"
    use_voice_output = input("Do you want to use voice output? (y/n): ").strip().lower() == "y"

    
    # Lists the available microphones if voice input is selected
    if use_voice_input:
        print("Available microphones:")
        list_microphones()
        mic_index = int(input("Enter the microphone index you want to use: "))

    main_agent = ModelWrapper(sys_prompt=sys_prompt, tools_access=True)

    start_message = {"role": "system", "content": "START OF AGENT INTERACTION - NO MESSAGES BEFORE THIS"}
    invoking_agent = ModelWrapper(sys_prompt=f"You are determining whether, in the most recent message, the user is most likely talking to their AI assistant or someone else. If you determine the user is talking to the AI, named {agent_name.title()}, respond with 'True'. Otherwise respond with 'False'. Remember that the user may be talking to themself or another person. Think if necessary, but your final response (True or False) should be on a new line. You have access to the most recent user-agent interactions to help you.", memory=[start_message], model="fast")
    awake_status_agent = ModelWrapper(sys_prompt=f"You are determining whether, in the most recent message, the user that is talking to their AI assistant wants to make the AI go to sleep or in any way stop the conversation. If you determine the user desires to end the session with the AI, named {agent_name.title()}, respond with 'True'. Otherwise respond with 'False'. Think as much as you want, but your final response (True or False) should be on a new line. You have access to the most recent user-agent interactions to help you.", memory=[start_message], model="fast")
    invoking_agent_memory_length = 6
    awake_agent_memory_length = 6

    running = True
    is_awake = True
    last_response = ""

    while running:
        is_invoked = False

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

        # Checks if the user would like to end the conversation, but allows the model a chance to respond
        if user_prompt.lower().strip() == break_word:
            running = False
        
        if is_awake:
            is_invoked, is_awake = call_listening_agents(user_prompt, last_response, invoking_agent, awake_status_agent, agent_name, invoking_agent_memory_length, awake_agent_memory_length)

            # Alerts the main agent that is is asleep to respond accordingly, if necessary
            if not is_awake:
                main_agent.add_memory("system", "You are now entering sleep mode. Please respond with a small amount of technical jargon that a robot would use when going to sleep, but be concise, around 3-5 words.")
                is_invoked = True

        print(f"User is {"NOT " if not is_invoked else ''}adressing the agent")
        print(agent_name.title() + (" is awake" if is_awake else " is sleeping"))
    
        # Main code - runs through tasks and generates new model response
        if (agent_name in user_prompt.lower() or is_invoked) and user_prompt != "":
            # Loops through all the completed tasks and adds them to the agent's memory
            for i in range(len(completed_tasks)):
                task, seen = completed_tasks[i]
                main_agent.add_memory("system", f"User question asking '{task}' has been completed and stored. Please alert the user.")

                completed_tasks[i] = (task, True)

            # Removes all tasks that have been seen by the agent
            completed_tasks[:] = [(task, False) for task, seen in completed_tasks if not seen]

            # Informs the user of the response status and generates a new response
            print(agent_name.title() + " is pondering...")
            agent_response = main_agent.call_model(user_prompt)
            tool_calls = agent_response.tool_calls

            while len(tool_calls) > 0:
                tool_messages = []
                for tool_call in tool_calls:
                    selected_tool = {tool.name: tool for tool in all_tools}[tool_call["name"].lower()]
                    tool_msg = selected_tool.invoke(tool_call)
                    tool_messages.append(tool_msg)

                main_agent.add_memories(tool_messages)
                agent_response = main_agent.call_model()
                tool_calls = agent_response.tool_calls

            response_content = agent_response.content

            # If the response contains the reason() method, it will start a new thread to process the question
            if "{reason()}" in response_content:
                # Alerts the user and formats the response
                print(f"{agent_name.upper()} INITIATED REASON MODE")
                response_content = response_content.replace("{reason()}", "")
                
                # Creates a new thread to respond to complex requests
                threading.Thread(target=think, daemon=True, args=(main_agent.format_memory_simple(), completed_tasks)).start()

                # Updates the models memory to give it information on the current status of the method
                main_agent.add_memory("system", "User question is currently being processed using the reason() method. You will be alerted once it is completed.")

            # Prints out the agent's response, without its thinking
            response_content = response_content.split('</think>')[-1].strip()
            print(f"{agent_name.title()}: {response_content}")

            # If voice output is selected, it will clear the speech event and speak the response
            if use_voice_output:
                stop_speech_event.clear()
                threading.Thread(target=speak, daemon=True, args=(response_content,)).start()

            # Wakes up the agent if the user directly adressed it - is_invoked can only be True if the agent in awake
            if not is_invoked:
                is_awake = True

            # Loads in the previous chat histories, including the current one if it exists
            with open(chat_log_file_path, 'r') as f:
                all_logs = json.load(f)

            # Overrides the chat history with the updated one
            all_logs[instance_id] = main_agent.format_memory()

            # Stores the updated history back to the json file
            with open(chat_log_file_path, 'w') as f:
                json.dump(all_logs, f, indent=4)

            last_response = response_content


if __name__ == "__main__":
    main()
