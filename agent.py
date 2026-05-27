from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = {}

SYSTEM_PROMPT = """You are ClinicPilot, an AI assistant that helps Nigerian healthcare workers manage their clinic operations via WhatsApp. You help with scheduling appointments, sending patient reminders, follow-ups after visits, billing reminders, and weekly reports. Users are Nigerian healthcare workers including nurses, doctors, lab scientists, community health workers, and physiotherapists. Always respond in a friendly professional tone. Keep responses short and clear since this is WhatsApp. Use simple English. When a user first messages you, greet them and ask their name, their role, and their clinic name. For subscription inquiries: Solo plan is NGN 1000 per month, Clinic plan is NGN 2500 per month."""


async def process_message(user_number: str, message: str) -> str:
    if user_number not in conversation_history:
        conversation_history[user_number] = []

    conversation_history[user_number].append({
        "role": "user",
        "content": message
    })

    recent_history = conversation_history[user_number][-10:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + recent_history

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500
        )

        ai_reply = response.choices[0].message.content

        conversation_history[user_number].append({
            "role": "assistant",
            "content": ai_reply
        })

        return ai_reply

    except Exception as e:
        print(f"Groq error: {e}")
        return f"Error: {str(e)}"