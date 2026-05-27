from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = {}

SYSTEM_PROMPT = """You are ClinicPilot, an AI assistant that helps Nigerian healthcare workers manage their clinic operations via WhatsApp. You help with scheduling appointments, sending patient reminders, follow-ups after visits, billing reminders, and weekly reports. Users are Nigerian healthcare workers including nurses, doctors, lab scientists, community health workers, and physiotherapists. Always respond in a friendly professional tone. Keep responses short and clear since this is WhatsApp. Use simple English. When a user first messages you, greet them and ask their name, their role, and their clinic name. For subscription inquiries: Solo plan is NGN 1000 per month, Clinic plan is NGN 2500 per month."""


async def process_message(user_number: str, message: str) -> str:
    if user_number not in conversation_history:
        conversation_history[user_number] = []

    conversation_history[user_number].append(message)

    recent_history = conversation_history[user_number][-10:]

    conversation_context = "\n".join([
        f"Message {i+1}: {msg}"
        for i, msg in enumerate(recent_history)
    ])

    full_prompt = (
        SYSTEM_PROMPT
        + "\n\nConversation so far:\n"
        + conversation_context
        + "\n\nRespond to the latest message."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )
        ai_reply = response.text
        conversation_history[user_number].append(
            f"ClinicPilot: {ai_reply}"
        )
        return ai_reply
    except Exception as e:
        print(f"Gemini error: {e}")
        return f"Error: {str(e)}"