# 📨 MiniMQ - A Minimal Message Broker in Go 🐹

**MiniMQ** is a lightweight, containerized **distributed messaging system** built with **Go**, **Python**, and **Flask**, now extended with **observability agents** that collect host-level system metrics (CPU, memory, disk) via Kubernetes **DaemonSets**.

It demonstrates microservice communication, message persistence, metric streaming, and web-based message consumption — all deployed on **Docker** or **Kubernetes**.

---

## ✨ What's New

- 🚀 **Kubernetes support** with Deployments, Services, and DaemonSets  
- 📊 **Node-level observability** via producers collecting real host metrics (using `psutil`)  
- 🧠 **Dynamic node registration** — each node self-registers with the broker automatically  
- 🖥️ **Dashboard per node** — visualize CPU, memory, and disk usage for every node in the cluster  
- 🧱 **Improved broker** with automatic directory creation and `/app/data` persistence  
- 🐳 **Docker Hub integration** for portable image deployment  
- 🔁 Backward-compatible with **Docker Compose** for local testing  

---

## 🏗 Architecture Overview

```
+------------------+         +------------------+         +----------------+
| Producer (CPU)   | --->    |                  | --->    |                |
| Producer (MEM)   | --->    |     Broker       | --->    |   Dashboard    |
| Producer (DISK)  | --->    |   (Go Server)    | --->    |   (Flask UI)   |
+------------------+         +------------------+         +----------------+
        ↑                            |
        |                            |
   (Runs on every node via)          |
        Kubernetes DaemonSet         |
```

Each node runs a set of producers (CPU, MEM, DISK) as DaemonSets.  
On startup, producers:
1. Register their **node name** with the broker (`topic="nodes"`).  
2. Stream metrics under topics like `<node>-cpu`, `<node>-mem`, and `<node>-disk`.  

The broker logs every message in `/app/data/<topic>.log`,  
and the Flask dashboard dynamically detects nodes and visualizes their metrics in real time.

---

## 📁 Project Structure

```
mini-mq/
│
├── broker/                 # Go-based message broker
│   ├── main.go
│   ├── handlers.go
│   ├── storage.go
│   ├── offset.go
│   ├── Dockerfile
│   └── data/               # Logs per topic (auto-created)
│
├── producer/               # Python-based metric producer
│   ├── producer.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── consumer/               # Flask-based dashboard UI
│   ├── app.py
│   ├── consumer_logic.py
│   ├── templates/
│   │   └── index.html
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/                    # Kubernetes manifests
│   ├── broker.yaml
│   ├── consumer.yaml
│   ├── producers-daemonset.yaml
│
├── docker-compose.yaml
└── README.md
```

---

## 🛠 Tools & Technologies

| Category          | Tool / Tech                         | Purpose / Notes |
|-------------------|-------------------------------------|-----------------|
| **Languages**     | Go, Python 3                        | Core services and metric agents |
| **Frameworks**    | Flask (Python)                      | Web-based consumer dashboard |
| **Containers**    | Docker, Docker Compose              | Local development setup |
| **Orchestration** | Kubernetes (Deployments, DaemonSets, Services) | Cluster-wide deployment |
| **Metrics**       | psutil (Python)                     | Host-level system metrics |
| **Persistence**   | File-based (`/app/data/*.log`)      | Per-topic message storage |
| **Logging**       | log (Go)                            | Structured logs |
| **CI/CD**         | Docker Hub                          | Image publishing |
| **Frontend**      | HTML + Bootstrap + Chart.js         | Live cluster dashboard |
| **API**           | REST (HTTP + JSON)                  | Communication protocol |

---

## 🚀 Running Locally (Docker Compose)

1. **Clone the repo**
   ```bash
   git clone https://github.com/LUI5DA/minimq-broker.git
   cd minimq-broker
   ```

2. **Build and start**
   ```bash
   docker compose up --build
   ```

3. **Access the UI**
   ```
   http://localhost:8080
   ```

   You’ll see CPU, memory, and disk metrics streaming in real time, with a simple dashboard per topic.

---

## ☸️ Running on Kubernetes (Recommended)

### 1️⃣ Build and push images
```bash
docker build -t lui5da/broker:latest ./broker
docker build -t lui5da/producer:latest ./producer
docker build -t lui5da/consumer:latest ./consumer

docker push lui5da/broker:latest
docker push lui5da/producer:latest
docker push lui5da/consumer:latest
```

### 2️⃣ Deploy to cluster
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/broker.yaml
kubectl apply -f k8s/consumer.yaml
kubectl apply -f k8s/producers-daemonset.yaml
```

### 3️⃣ Monitor status
```bash
kubectl get pods -n minimq
kubectl get svc -n minimq
```

### 4️⃣ Open dashboard
```
http://<EXTERNAL-IP>:8080
```

<img width="1919" height="952" alt="Screenshot From 2025-10-22 18-56-56" src="https://github.com/user-attachments/assets/bd8e5625-99fd-4c57-9d47-656b6b957269" />


You’ll see a **card for each node** in your cluster with live metrics for CPU, memory, and disk.

---

## 📊 Node-Level Observability

| DaemonSet | Metric | Description |
|------------|---------|-------------|
| `producer-host-cpu`  | CPU usage (%)   | Collects average CPU load per node |
| `producer-host-mem`  | Memory usage (%)| Collects memory utilization per node |
| `producer-host-disk` | Disk usage (%)  | Collects filesystem utilization per node |

### How it works:
- On startup, producers register their **node name** with the broker (`topic="nodes"`).  
- Metrics are sent to the broker at intervals (e.g., every 1–5 seconds).  
- The broker stores them in `data/<node>-<metric>.log`.  
- The Flask dashboard queries `/nodes` to dynamically discover nodes  
  and fetches their latest metrics from `/consume`.

---

## 📈 Dashboard Overview

The Flask dashboard automatically visualizes each node’s metrics:

```
📊 MiniMQ Cluster Dashboard

🖥️ node-1
───────────────────────────────
CPU Usage:   45.3%
Memory:      71.8%
Disk Usage:  12.4%
(graphs...)

🖥️ node-2
───────────────────────────────
CPU Usage:   33.1%
Memory:      64.9%
Disk Usage:  14.7%
```

✅ Live updating every 2 seconds  
✅ Automatic node discovery  
✅ Separate colors and labels per metric (blue = CPU, green = MEM, orange = DISK)

---

## 🧰 Useful Kubernetes Commands

```bash
# View logs
kubectl logs -n minimq -l app=broker
kubectl logs -n minimq -l app=producer-host-cpu
kubectl logs -n minimq -l app=producer-host-mem
kubectl logs -n minimq -l app=producer-host-disk

# Restart deployments
kubectl rollout restart deployment broker -n minimq
kubectl rollout restart deployment consumer -n minimq

# Access broker shell
kubectl exec -it $(kubectl get pod -l app=broker -n minimq -o name) -n minimq -- /bin/bash
```

---

## 👨‍💻 Author

**LUI5DA**  
Systems Engineering Student — Universidad Nacional de Costa Rica  
> Exploring distributed systems, Kubernetes, and observability through Go and Python microservices.
