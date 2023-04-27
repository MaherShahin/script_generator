import subprocess

class ScriptValidator:
    def __init__(self):
        pass

    def validate(self, code):
        # Check for the presence of the shebang line
        shebang_line = "#!/bin/bash"
        if shebang_line not in code:
            return False

        # Check for syntax errors using the 'bash -n' command
        try:
            with subprocess.Popen(["bash", "-n"], stdin=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                _, stderr = proc.communicate(input=code.encode())

            if stderr:
                print(f"Syntax errors found:\n{stderr.decode()}")
                return False
        except Exception as e:
            print(f"Error occurred while checking syntax: {e}")
            return False

        return True