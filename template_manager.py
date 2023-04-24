import json

class TemplateManager:
    def __init__(self):
        with open("prompts.json", "r") as f:
            self.prompts = json.load(f)

    def load_template(self, prompt_type):
        if prompt_type not in self.prompts:
            print(f"Prompt type {prompt_type} does not exist.")
            return None
        return self.prompts[prompt_type]["template"]

    def get_template_variables(self, prompt_type):
        if prompt_type not in self.prompts:
            print(f"Prompt type {prompt_type} does not exist.")
            return None
        return self.prompts[prompt_type]["variables"]
