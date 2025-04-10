from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_response( message: str):
    print("Message is ",message)
    default_message = "Calculate the sum of exponentials of first 3 Fibonacci numbers"
    if len(message.strip()) == 0:
        print("Message is empty")
        message = default_message
    print("Message is ",message)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
    )
    return response.text
