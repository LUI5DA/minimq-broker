# consumer_logic.py

import requests

BROKER_URL = "http://localhost:5000"
TOPIC = "temperature"
CONSUMER_ID = "web-ui"

def get_next_message():
    try:
        res = requests.get(
            f"{BROKER_URL}/consume",
            params={"topic": TOPIC, "consumer_id": CONSUMER_ID}
        )
        print(f"[Broker Response] Status: {res.status_code} - {res.text}")  # 🔍 Add this
        if res.status_code == 200:
            data = res.json()
            return data["message"]
        else:
            return None
    except Exception as e:
        print(f"[✘] Error polling broker: {e}")
        return None
