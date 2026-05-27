import httpx
import os
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")

PLANS = {
    "solo": {
        "name": "ClinicPilot Solo",
        "amount": 100000,  # NGN 1,000 in kobo
        "description": "Solo plan for individual healthcare workers"
    },
    "clinic": {
        "name": "ClinicPilot Clinic",
        "amount": 250000,  # NGN 2,500 in kobo
        "description": "Clinic plan for small clinics"
    }
}

async def create_payment_link(
    email: str,
    plan: str,
    user_name: str
) -> str:
    url = "https://api.paystack.co/transaction/initialize"
    
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }
    
    plan_details = PLANS.get(plan, PLANS["solo"])
    
    payload = {
        "email": email,
        "amount": plan_details["amount"],
        "currency": "NGN",
        "metadata": {
            "custom_fields": [
                {
                    "display_name": "Customer Name",
                    "variable_name": "customer_name",
                    "value": user_name
                },
                {
                    "display_name": "Plan",
                    "variable_name": "plan",
                    "value": plan_details["name"]
                }
            ]
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, 
            json=payload, 
            headers=headers
        )
        data = response.json()
        
        if data["status"]:
            return data["data"]["authorization_url"]
        else:
            return "Payment link generation failed"
        
        