import httpx
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"
}

r = httpx.get("https://api.paystack.co/bank", headers=headers)
print("Paystack connected:", r.status_code == 200)