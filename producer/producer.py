from config import BROKER_URL, TOPICS, INTERVAL_SECONDS
import random, time, requests

def generate_value():
    return random.randint(20, 100)

def choose_topic():
    return random.choice(TOPICS)

def send_message(topic, value):
    payload = {
        "topic": topic,
        "message": str(value)
    }
    try:
        res = requests.post(BROKER_URL, json=payload)
        if res.status_code == 201:
            print(f"[✔] Sent to {topic}: {value}")
        else:
            print(f"[!] Failed ({res.status_code})")
    except Exception as e:
        print(f"[✘] Error: {e}")

def run():
    while True:
        topic = choose_topic()
        value = generate_value()
        send_message(topic, value)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()
