from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import os
from dotenv import load_dotenv
from tools import all_tools
from groq import RateLimitError, APIStatusError
import json

load_dotenv()

# Load in the meta info to be used later
with open("meta_info.json", "r") as f:
    meta_info = json.load(f)

# Create a list of commonly used llms to avoid having to reinitialize at agent creation
base_llm = init_chat_model("meta-llama/llama-4-maverick-17b-128e-instruct", model_provider="groq")
backup_llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq")
fast_llm = init_chat_model("llama-3.1-8b-instant", model_provider="groq")

model_registry = {
    "base": base_llm,
    "backup": backup_llm,
    "fast": fast_llm
}

message_type_registry = {
    "user": HumanMessage,
    "assistant": AIMessage,
    "system": SystemMessage,
    "tool": ToolMessage
}

api_key_registry = {
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google_genai": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY"
}


class ModelWrapper:
    def __init__(self, sys_prompt="", memory=None, model="base", model_provider="groq", tools_access=False, max_messages=1000, max_tokens=100000, memory_buffer=2, summarize_memory=True):
        temp_memory = []
        temp_memory.append(SystemMessage(sys_prompt)) if sys_prompt else None
        temp_memory += [message_type_registry.get(msg["role"])(msg["content"]) for msg in memory] if memory is not None else []
        
        self.memory = temp_memory

        self.has_sys_prompt = sys_prompt != "" and sys_prompt is not None

        self.model = model
        self.model_provider = model_provider
        
        if model not in model_registry.keys():
            llm = init_chat_model(model, model_provider=model_provider)
        else:
            llm = model_registry[model]

        if tools_access: llm = llm.bind_tools(all_tools)
        self.llm = llm

        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.memory_buffer = memory_buffer

        self.summarize_meory = summarize_memory

    def add_memory(self, role, content):
        new_memory = message_type_registry.get(role)(content)
        self.memory.append(new_memory)

    def add_memories(self, new_memories):
        self.memory += new_memories

    def format_memory(self):
        reversed_message_type_registry = {value: key for key, value in message_type_registry.items()}
        formatted_memory = [{(reversed_message_type_registry[type(message)] if type(message) in reversed_message_type_registry.keys() else "other"): vars(message)} for message in self.memory]
        return formatted_memory
    
    def format_memory_simple(self):
        reversed_message_type_registry = {value: key for key, value in message_type_registry.items()}
        reversed_message_type_registry[ToolMessage] = "system"
        formatted_memory = [{"role": (reversed_message_type_registry[type(message)] if type(message) in reversed_message_type_registry.keys() else "system"), "content": vars(message)["content"]} for message in self.memory]
        return formatted_memory

    def compact_memory(self):
        new_memory = self.memory[-self.memory_buffer:]

        if self.summarize_meory:
            summarizer_memory = self.memory[:-self.memory_buffer] + [HumanMessage(''.join(meta_info["summarizing_prompt"]))]
            summary = self.llm.invoke(summarizer_memory)
            print("MEMORY SUMMARIZED")

            new_memory = summary + new_memory

        if self.has_sys_prompt:
            new_memory = self.memory[0] + new_memory

        self.memory = new_memory.messages

        print("MEMORY COMPACTED")

    def call_model(self, content="", store_prompt=True, store_response=True, prompt_role="user"):
        prompt = message_type_registry.get(prompt_role)(content) if content != "" and content is not None else None
        messages = self.memory + ([prompt] if prompt is not None else [])

        response = None

        i = 1
        while f"{api_key_registry[self.model_provider]}_{i}" in os.environ and response is None:
            os.environ[api_key_registry[self.model_provider]] = os.getenv(f"{api_key_registry[self.model_provider]}_{i}")
            try:
                response = self.llm.invoke(messages)
            except (RateLimitError, APIStatusError):
                pass
            i += 1

        if response is not None:
            usage_metadata = response.usage_metadata
            memory_tokens = usage_metadata["input_tokens"]

            if store_prompt and prompt is not None:
                self.memory.append(prompt)
            if store_response:
                self.memory.append(response)
                memory_tokens += usage_metadata["output_tokens"]

            if (memory_tokens > self.max_tokens and self.max_tokens > 0) or (len(self.memory) > self.max_messages and self.max_messages > 0):
                print("OVERFLOW", memory_tokens)
                self.compact_memory()


        return response
