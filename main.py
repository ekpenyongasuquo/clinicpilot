from fastapi import FastAPI, Request, Query
from fastapi.responses import PlainTextResponse
import os
from dotenv import load_dotenv
from agent import process_message
from whatsapp import send_whatsapp_message

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Webhook verification - Meta calls this once to confirm your server
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)
    return PlainTextResponse(content="Forbidden", status_code=403)

# Webhook receiver - Meta sends messages here
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            
            if message["type"] == "text":
                user_text = message["text"]["body"]
                
                # Get AI response from Gemini agent
                ai_response = await process_message(
                    user_number=from_number,
                    message=user_text
                )
                
                # Send response back via WhatsApp
                await send_whatsapp_message(
                    to=from_number,
                    message=ai_response
                )
    except Exception as e:
        print(f"Error processing message: {e}")
    
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "ClinicPilot is running"}