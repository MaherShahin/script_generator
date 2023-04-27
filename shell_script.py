import os
import re

class ShellScript:
    
    def __init__(self, code):
        self.code = code

    def sanitize(self):
        # Remove text before and including the start delimiter (```bash)
        start_delimiter = "```bash"
        start_index = self.code.find(start_delimiter)
        if start_index == -1:
            raise ValueError("Start delimiter (```bash) not found in the code.")
        self.code = self.code[start_index + len(start_delimiter):]

        # Remove text after and including the end delimiter (```)
        end_delimiter = "```"
        end_index = self.code.rfind(end_delimiter)
        if end_index == -1:
            raise ValueError("End delimiter (```) not found in the code.")
        self.code = self.code[:end_index]

        # Remove any leading and trailing whitespace
        self.code = self.code.strip()

        # Check for any potentially harmful commands
        harmful_commands = ["rm ", "mv ", "dd ", "shutdown", "reboot", "init ", "kill"]
        for cmd in harmful_commands:
            if cmd in self.code:
                raise ValueError(f"Harmful command '{cmd}' detected in the code. Please review the script and remove or replace it before running.")


        
    def save(self, path="generated_scripts/script.sh"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(self.code)

    def __str__(self):
        return f"\nHere is the shell script with comments as requested:\n\n{self.code}\n"
