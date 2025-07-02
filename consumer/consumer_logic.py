# consumer_logic.py

import requests

#BROKER_URL = "http://localhost:5000"
BROKER_URL = "http://broker:5000"
TOPIC = "temperature"
CONSUMER_ID = "web-ui"

def get_next_message(topic):
    try:
        res = requests.get(
            f"{BROKER_URL}/consume",
            params={"topic": topic, "consumer_id": CONSUMER_ID}
        )
        if res.status_code == 200:
            return res.json()["message"]
    except Exception as e:
        print(f"[Error] {e}")
    return None
