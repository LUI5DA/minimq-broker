import os
import time
import psutil
import requests

# === Environment configuration ===
BROKER_URL = os.getenv("BROKER_URL", "http://broker:5000/produce")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "1"))
METRIC_TYPE = os.getenv("METRIC_TYPE", "cpu").lower()
NODE_NAME = os.getenv("NODE_NAME", "unknown-node")

# === Host mode configuration ===
# If running in host mode (DaemonSet with /host_proc mount), direct psutil to read from host /proc
if os.getenv("HOST_MODE", "false").lower() == "true":
    if os.path.exists("/host_proc"):
        psutil.PROCFS_PATH = "/host_proc"
        print("[⚙️] HOST_MODE enabled: using /host_proc for metrics")
    else:
        print("[!] HOST_MODE set but /host_proc not mounted")


# === Metric collection functions ===

def get_cpu_usage():
    """Returns average CPU usage across all cores (percentage)."""
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    avg_cpu = sum(per_cpu) / len(per_cpu)
    return round(avg_cpu, 2)


def collect_metric(metric_type: str):
    """Collects the specified metric from the host system."""
    if metric_type == "cpu":
        return get_cpu_usage()
    elif metric_type == "mem":
        return psutil.virtual_memory().percent
    elif metric_type == "disk":
        return psutil.disk_usage("/").percent
    elif metric_type == "net":
        counters = psutil.net_io_counters()
        return {"bytes_sent": counters.bytes_sent, "bytes_recv": counters.bytes_recv}
    else:
        print(f"[!] Unknown metric type '{metric_type}', defaulting to 'cpu'")
        return get_cpu_usage()


# === Message sending logic ===

def send_message(url, topic: str, value):
    """Sends a JSON message to the broker with topic and metric value."""
    payload = {"topic": topic, "message": str(value)}
    try:
        res = requests.post(BROKER_URL, json=payload, timeout=5)
        if res.status_code == 201:
            print(f"[✔] Sent to topic '{topic}': {value}")
        else:
            print(f"[!] Failed ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"[✘] Error sending message: {e}")


# === Main producer loop ===

def run():
    print(f"[+] Producer starting... node='{NODE_NAME}', metric='{METRIC_TYPE}', broker={BROKER_URL}")

    # (1) Register node at startup (only once)
    print(f"[→] Registering node '{NODE_NAME}' in broker node list")
    send_message(BROKER_URL, "nodes", NODE_NAME)

    # (2) Enter infinite loop to send metrics
    while True:
        value = collect_metric(METRIC_TYPE)
        topic = f"{NODE_NAME}-{METRIC_TYPE}"
        send_message(topic, value)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
