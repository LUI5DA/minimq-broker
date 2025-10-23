# consumer/consumer_logic.py
import requests

BROKER_URL = "http://broker:5000"
CONSUMER_ID = "web-ui"

def get_nodes():
    """Return the list of available nodes from the broker."""
    try:
        res = requests.get(f"{BROKER_URL}/nodes", timeout=5)
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        print(f"[Error getting nodes] {e}")
        return []

def get_metric_value(node, metric):
    """Fetch the latest metric for a given node and type."""
    topic = f"{node}-{metric}"
    try:
        res = requests.get(
            f"{BROKER_URL}/consume",
            params={"topic": topic, "consumer_id": CONSUMER_ID},
            timeout=5
        )
        if res.status_code == 200:
            return res.json().get("message")
    except Exception as e:
        print(f"[Error getting {topic}] {e}")
    return None
