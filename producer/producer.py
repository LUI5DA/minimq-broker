# producer.py

import time
import json
import random
import requests
from config import BROKER_URL, TOPIC, INTERVAL_SECONDS

def generate_temperature():
    return round(random.uniform(20.0, 30.0), 1)

def send_message(value):
    payload = {
        "topic": TOPIC,
        "message": str(value)
    }
    try:
        response = requests.post(BROKER_URL, json=payload)
        if response.status_code == 201:
            print(f"[✔] Sent: {value}")
        else:
            print(f"[!] Failed to send: {response.text}")
    except Exception as e:
        print(f"[✘] Error: {e}")

def run():
    while True:
        value = generate_temperature()
        send_message(value)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()
