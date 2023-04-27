class ShellScriptGenerator:
    def __init__(self, gpt_client):
        self.gpt_client = gpt_client

    def generate_shell_script(self, choice, messages):
        generation_request = [
            *messages,
            {
                "role": "system",
                "content": f"User has chosen plan {choice}. Please generate a shell script based on the chosen plan. Generate a shell script that solves the problem, fulfills the constraints, and meets the acceptance criteria. Generate only shell code, dont provide any explanations but make sure your shell script is well commented.",
            },
        ]
        shell_code_response = self.gpt_client.query_gpt(messages=generation_request)

        if not shell_code_response:
            print("Failed to generate the shell script.")
            return None

        shell_code = shell_code_response["choices"][0]["message"]["content"]
        return shell_code
