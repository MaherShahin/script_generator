import openai
from dotenv import load_dotenv
import os

class GPTClient:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query_gpt(self, messages, max_tokens=1000, temperature=0.5):
        try:
            if not (0 < max_tokens <= 2048):
                raise ValueError("max_tokens should be within the range (0, 2048]")

            if not (0 < temperature <= 1):
                raise ValueError("temperature should be within the range (0, 1]")

            response = openai.ChatCompletion.create(
                engine="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            result = response.choices[0].text.strip()

            if not result:
                raise ValueError("The GPT-4 model returned an empty or incomplete response")

            return result

        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"An error occurred while querying the GPT-4 model: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None