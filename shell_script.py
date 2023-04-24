import os
import re

class ShellScript:
    def __init__(self, code):
        self.code = code

    def sanitize(self):
        self.code = re.sub(r'[^#\w\s\.\-/]+', '', self.code)

    def save(self, directory="generated_scripts", filename="script.sh"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, filename), "w") as script_file:
            script_file.write(self.code)
