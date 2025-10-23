# 📨 MiniMQ - A Minimal Message Broker in Go 🐹

**MiniMQ** is a lightweight, containerized **distributed messaging system** built with **Go**, **Python**, and **Flask**, now extended with **observability agents** that collect host-level system metrics (CPU, memory, disk) via Kubernetes **DaemonSets**.

It demonstrates microservice communication, message persistence, metric streaming, and web-based message consumption — all deployed on **Docker** or **Kubernetes**.

---

## ✨ What's New

- 🚀 **Kubernetes support** with Deployments, Services, and DaemonSets  
- 📊 **System observability** via producers collecting real host metrics (using `psutil`)  
- 🧠 **DaemonSet producers** running on every node to stream CPU, memory, and disk usage  
- 🧱 **Improved broker** with automatic log directory creation and persistent `/app/data` storage  
- 🐳 **Docker Hub integration** for portable image deployment  
- 💻 **Dashboard UI** (Flask) to visualize messages and metrics  
- 🔁 Backward-compatible with **Docker Compose** for local testing  

---

## 🏗 Architecture Overview

```
+-----------------+        +-----------------+        +----------------+
| Producer (CPU)  | --->   |                 | --->   |                |
| Producer (MEM)  | --->   |     Broker      | --->   |   Consumer UI  |
| Producer (DISK) | --->   |   (Go Server)   | --->   |  (Flask App)   |
+-----------------+        +-----------------+        +----------------+
          ^                        |
          |                        |
   (Runs on every node via)        |
        Kubernetes DaemonSet       |
```

Each producer is a small Python container that reads host metrics using `psutil` and publishes them to the Go broker via HTTP.  
The broker logs all messages in `/app/data/<topic>.log`, and the Flask consumer visualizes them in a live dashboard.

---

## 📁 Project Structure

```
mini-mq/
│
├── broker/               # Go-based message broker
│   ├── main.go
│   ├── handlers.go
│   ├── storage.go
│   ├── offset.go
│   ├── Dockerfile
│   └── data/             # Logs per topic (auto-created)
│
├── producer/             # Python-based producer (metric collector)
│   ├── producer.py
│   ├── config.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── consumer/             # Flask-based dashboard UI
│   ├── app.py
│   ├── consumer_logic.py
│   ├── templates/
│   │   └── index.html
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/           # Manifests for K8s deployment
│   ├── broker.yaml
│   ├── consumer.yaml
│   ├── producer.yaml
│
├── docker-compose.yaml   # For local development
└── README.md
```

---

## 🛠 Tools & Technologies

| Category          | Tool / Tech                         | Purpose / Notes |
|-------------------|-------------------------------------|-----------------|
| **Languages**     | Go, Python 3                        | Core microservices and metric agents |
| **Frameworks**    | Flask (Python)                      | Web-based consumer dashboard |
| **Containers**    | Docker, Docker Compose              | Local development setup |
| **Orchestration** | Kubernetes (Deployments, DaemonSets, Services) | Cluster-wide deployment |
| **Metrics**       | psutil (Python)                     | Host-level system metrics |
| **Persistence**   | File-based (`/app/data/*.log`)      | Per-topic message storage |
| **Logging**       | log (Go)                            | Structured logs |
| **CI/CD**         | Docker Hub                          | Build and push images |
| **Frontend**      | HTML + Bootstrap                    | Simple responsive UI |
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
   You’ll see CPU, memory, and disk metrics streaming in real time.

---

## ☸️ Running on Kubernetes

### 1️⃣ Push images to Docker Hub
Make sure all images are built and pushed:
```bash
docker build -t lui5da/broker:latest ./broker
docker build -t lui5da/producer:latest ./producer
docker build -t lui5da/consumer:latest ./consumer

docker push lui5da/broker:latest
docker push lui5da/producer:latest
docker push lui5da/consumer:latest
```

### 2️⃣ Apply Kubernetes manifests
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/broker.yaml
kubectl apply -f kubernetes/consumer.yaml
kubectl apply -f kubernetes/producers-daemonset.yaml
```

### 3️⃣ Check status
```bash
kubectl get pods -n minimq
kubectl get svc -n minimq
```

### 4️⃣ Access the dashboard
If you’re using a cloud provider:
```
http://<EXTERNAL-IP>:8080
```

---

## 📊 Observability (via DaemonSets)

| DaemonSet | Metric | Description |
|------------|---------|-------------|
| `producer-host-cpu`  | CPU usage (%)   | Collects host CPU metrics every second |
| `producer-host-mem`  | Memory usage (%)| Collects host memory stats every 5 seconds |
| `producer-host-disk` | Disk usage (%)  | Collects host disk utilization every 5 seconds |

Each node in the cluster runs one instance of each DaemonSet, ensuring cluster-wide visibility.

All metrics are sent to the broker endpoint:
```
http://broker:5000/produce
```
and stored in `/app/data/<topic>.log`.

---

## 🧰 Useful Kubernetes Commands

```bash
# View logs for all producers
kubectl logs -n minimq -l app=producer-host-cpu
kubectl logs -n minimq -l app=producer-host-mem
kubectl logs -n minimq -l app=producer-host-disk

# Restart deployments
kubectl rollout restart deployment broker -n minimq

# Enter broker container
kubectl exec -it $(kubectl get pod -l app=broker -n minimq -o name) -n minimq -- /bin/bash
```

---

## 🧠 Future Improvements

- 📈 Add Prometheus/Grafana exporters for real-time visualization  
- ☁️ Helm chart for automated deployments  
- 🔐 Add authentication and rate limiting to the broker API  
- 🧩 Integrate persistent storage (PVC) for broker logs  

---

## 👨‍💻 Author

**LUI5DA**  
Systems Engineering Student — Universidad Nacional de Costa Rica  
> Exploring distributed systems, Kubernetes, and observability through Go and Python microservices.