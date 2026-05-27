from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def process_message(user_number: str, message: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser message: {message}"
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "Sorry, I am having trouble right now. Please try again."