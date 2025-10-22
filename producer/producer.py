import os
import time
import psutil
import requests

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
from config import BROKER_URL, INTERVAL_SECONDS
METRIC_TYPE = os.getenv("METRIC_TYPE", "cpu").lower()

# -----------------------------------------------------------------------------
# Metric collection logic
# -----------------------------------------------------------------------------
def collect_metric(metric_type):
    """
    Collect a system metric depending on METRIC_TYPE.
    Supported: cpu, mem, disk, net
    """ 
    if metric_type == "cpu":
        return psutil.cpu_percent(interval=1)
    elif metric_type == "mem":
        return psutil.virtual_memory().percent
    elif metric_type == "disk":
        return psutil.disk_usage("/").percent
    elif metric_type == "net":
        counters = psutil.net_io_counters()
        return {"bytes_sent": counters.bytes_sent, "bytes_recv": counters.bytes_recv}
    else:
        print(f"[!] Unknown metric type '{metric_type}', defaulting to 'cpu'")
        return psutil.cpu_percent(interval=1)

# -----------------------------------------------------------------------------
# Communication with broker
# -----------------------------------------------------------------------------
def send_message(topic, value):
    """
    Send the collected metric to the broker.
    """
    payload = {"topic": topic, "message": str(value)}
    try:
        res = requests.post(BROKER_URL, json=payload, timeout=5)
        if res.status_code == 201:
            print(f"[✔] Sent to topic '{topic}': {value}")
        else:
            print(f"[!] Failed ({res.status_code}): {res.text}")
    except requests.exceptions.ConnectionError:
        print(f"[✘] Connection Error: Cannot reach broker at {BROKER_URL}")
    except requests.exceptions.Timeout:
        print(f"[✘] Timeout Error: Broker took too long to respond")
    except Exception as e:
        print(f"[✘] Unexpected Error: {e}")

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
def run():
    print(f"Producer starting... metric='{METRIC_TYPE}'")
    print(f"Broker URL: {BROKER_URL}")
    print(f"Interval: {INTERVAL_SECONDS}s\n")

    while True:
        value = collect_metric(METRIC_TYPE)
        send_message(METRIC_TYPE, value)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()
