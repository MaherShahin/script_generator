import openai
from dotenv import load_dotenv
import os

class GPTClient:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query_gpt(self, messages, max_tokens=150, temperature=0.5):
        try:
            if not (0 < max_tokens <= 4096):
                raise ValueError("max_tokens should be within the range (0, 4096]")

            if not (0 < temperature <= 1):
                raise ValueError("temperature should be within the range (0, 1]")

            formatted_messages = []
            for i, message in enumerate(messages):
                if i == 0:
                    formatted_messages.append({"role": "system", "text": message})
                else:
                    formatted_messages.append({"role": "user", "text": message})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                prompt=formatted_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            result = response.choices[0].text.strip()

            if not result:
                raise ValueError("The GPT-3.5 Turbo model returned an empty or incomplete response")

            return result

        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"An error occurred while querying the GPT-3.5 Turbo model: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None
