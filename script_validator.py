import subprocess

class ScriptValidator:
    def __init__(self):
        pass

    def validate(self, shell_script):
        try:
            # Run the shell script with the 'bash -n' command, which checks the syntax without executing the script
            result = subprocess.run(["bash", "-n"], input=shell_script, text=True, capture_output=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
