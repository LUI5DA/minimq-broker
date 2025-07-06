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
        res = requests.post(BROKER_URL, json=payload, timeout=5)
        if res.status_code == 201:
            print(f"[✔] Sent to {topic}: {value}")
        else:
            print(f"[!] Failed ({res.status_code}): {res.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"[✘] Connection Error: Cannot reach broker at {BROKER_URL}")
    except requests.exceptions.Timeout as e:
        print(f"[✘] Timeout Error: Broker took too long to respond")
    except Exception as e:
        print(f"[✘] Unexpected Error: {e}")

def run():
    print(f"Producer starting... Will send to {BROKER_URL}")
    print(f"Topics: {TOPICS}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    
    while True:
        topic = choose_topic()
        value = generate_value()
        send_message(topic, value)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()
