from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from tools import all_tools

load_dotenv()

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
    def __init__(self, sys_prompt="", memory=None, model="meta-llama/llama-4-maverick-17b-128e-instruct", model_provider="groq", tools_access=False):
        temp_memory = []
        temp_memory.append(SystemMessage(sys_prompt)) if sys_prompt else None
        temp_memory += [message_type_registry.get(msg["role"])(msg["content"]) for msg in memory] if memory is not None else []
        
        self.memory = temp_memory

        self.model = model
        self.model_provider = model_provider

        self.tools = all_tools.copy() if tools_access else []

    def add_memory(self, role, content):
        new_memory = message_type_registry.get(role)(content)
        self.memory.append(new_memory)

    def add_memories(self, new_memories):
        self.memory += new_memories

    def format_memory(self):
        reversed_message_type_registry = {value: key for key, value in message_type_registry.items()}
        formatted_memory = [{(reversed_message_type_registry[type(message)] if type(message) in reversed_message_type_registry.keys() else "other"): vars(message)} for message in self.memory]
        return formatted_memory

    def call_model(self, content="", store_prompt=True, store_response=True, prompt_role="user"):
        prompt = message_type_registry.get(prompt_role)(content) if content != "" and content is not None else None
        messages = self.memory + ([prompt] if prompt is not None else [])

        os.environ[api_key_registry[self.model_provider]] = os.getenv(f"{api_key_registry[self.model_provider]}_1")

        llm = init_chat_model(self.model, model_provider=self.model_provider)
        if len(self.tools) > 0: llm = llm.bind_tools(self.tools)

        response = llm.invoke(messages)

        if store_prompt and prompt is not None:
            self.memory.append(prompt)
        if store_response:
            self.memory.append(response)

        return response
