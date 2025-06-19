from model_caller import call_model

class ModelWrapper:
    def __init__(self, sys_prompt="", memory=None, model="meta-llama/llama-4-maverick-17b-128e-instruct"):
        temp_memory = []
        temp_memory.append({"role": "system", "content": sys_prompt}) if sys_prompt else None
        temp_memory += memory if memory is not None else []
        self.memory = temp_memory

        self.model = model

    def call_model(self, prompt="", store_prompt=True, store_response=True, prompt_role="user"):
        if store_prompt:
            self.memory.append({"role": prompt_role, "content": prompt})

        response = call_model(self.memory, model=self.model)

        if store_response:
            self.memory.append({"role": "assistant", "content": response})

        return response
