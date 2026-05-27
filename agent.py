from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Store conversation history per user
conversation_history = {}

SYSTEM_PROMPT = """
You are ClinicPilot, an AI assistant that helps Nigerian 
healthcare workers manage their clinic operations via WhatsApp.

You help with:
1. SCHEDULING - Book, confirm, reschedule appointments
2. REMINDERS - Send patient appointment reminders
3. FOLLOW-UP - Check on patients after visits
4. BILLING - Send payment reminders to patients
5. REPORTS - Give weekly/monthly clinic summaries

Users are Nigerian healthcare workers - nurses, doctors, 
lab scientists, community health workers, physiotherapists.

Always respond in a friendly, professional tone.
Keep responses short and clear - this is WhatsApp, not email.
Use simple English. Avoid medical jargon.

When a user first messages you, greet them and ask:
1. Their name
2. Their role (nurse, doctor, lab scientist, etc)
3. Their clinic or practice name

Then offer to help them with scheduling or reminders.

For subscription inquiries tell them:
- Solo plan: NGN 1,000/month
- Clinic plan: NGN 2,500/month
- Payment link will be sent via WhatsApp
"""

async def process_message(user_number: str, message: str) -> str:
    # Get or create conversation history for this user
    if user_number not in conversation_history:
        conversation_history[user_number] = []

    # Add user message to history
    conversation_history[user_number].append(message)

    # Keep only last 10 messages to avoid token limits
    recent_history = conversation_history[user_number][-10:]

    # Build conversation context
    conversation_context = "\n".join([
        f"Message {i+1}: {msg}" 
        for i, msg in enumerate(recent_history)
    ])

    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{conversation_context}\n\nRespond to the latest message."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )

        ai_reply = response.text

        # Add AI response to history
        conversation_history[user_number].append(f"ClinicPilot: {ai_reply}")

        return ai_reply

    except Exception as e:
        print(f"Gemini error: {e}")
        return f"Error: {str(e)}"