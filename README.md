# 📨 MiniMQ - A Minimal Message Broker in Go 🐹

MiniMQ is a lightweight, containerized **distributed messaging system** built from scratch using Go, Python, and Flask — inspired by Kafka-style pub/sub architectures.

It showcases core concepts of microservices, message persistence, concurrent message handling, and simple UI-based message consumption.

---

## 📦 Architecture Overview

```
[ producer (Python) ] --->     [          ]
[ producer (Python) ] ----->   [  broker  ] ---> [ consumer UI (Flask) ]
[ producer (Python) ] ----->   [  (Go)    ] ---> [ ...future consumers ]
                               [          ]
```

---

## ✨ Features

- ✅ Message broker in **Go**
- ✅ Support for **multiple topics**
- ✅ Persistent message logs (by topic)
- ✅ In-memory **consumer offset tracking**
- ✅ Concurrent-safe writing with **mutexes**
- ✅ Multiple producers sending randomly to topics
- ✅ Flask-based **consumer UI** with topic selection
- ✅ Fully containerized using **Docker Compose**

---

## 📁 Project Structure

```
mini-mq/
│
├── broker/           # Core message broker (Go)
│   ├── main.go
│   ├── handlers.go
│   ├── storage.go
│   ├── offset.go
│   ├── models.go
│   ├── Dockerfile
│   └── data/         # Logs per topic
│
├── producer/         # Simulated producer (Python)
│   ├── producer.py
│   ├── config.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── consumer/         # Super Simple Web UI for consuming messages (Python Flask)
│   ├── app.py
│   ├── consumer_logic.py
│   ├── templates/
│   ├── static/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yaml
└── README.md
```

---
# 🛠 Tools & Technologies Used

| Category          | Tool / Tech                         | Purpose / Notes                                 |
| ----------------- | ----------------------------------- | ----------------------------------------------- |
| **Language**      | Go (Golang)                         | Core message broker logic — fast and concurrent |
| **Language**      | Python 3.x                          | Producer and consumer logic                     |
| **Framework**     | Flask                               | Web-based UI for consuming messages             |
| **Containers**    | Docker                              | Containerization of all services                |
| **Orchestration** | Docker Compose                      | Multi-container setup and service linking       |
| **HTTP Client**   | `requests` (Python lib)             | For sending messages to the broker              |
| **Concurrency**   | `sync.Mutex` (Go)                   | Ensures safe concurrent writes to log files     |
| **Persistence**   | Local filesystem + file logs        | Messages are stored by topic in `.log` files    |
| **Templating**    | Jinja2 (via Flask)                  | For rendering the web UI                        |
| **API Protocol**  | REST (HTTP + JSON)                  | Simple and human-readable producer/consumer API |
| **Logging**       | `log` (Go) & print statements       | Simple CLI logging                              |
| **Frontend**      | HTML + Bootstrap (optional styling) | Used in the message consumer UI                 |

--

## 🚀 Running the Project (with Docker)

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/mini-mq.git
cd mini-mq
```

2. **Make sure Docker is installed**, then run:

```bash
docker compose up --build
```

3. Open the UI:

> 🌐 http://localhost:8080  
> Use the dropdown to select topics (e.g., `temperature`, `humidity`, `pressure`)

---

## 🧪 Simulating Multiple Producers

You can define more producers in `docker-compose.yaml` like this:

```yaml
producer1:
  build: ./producer
  environment:
    - TOPIC=temperature

producer2:
  build: ./producer
  environment:
    - TOPIC=humidity
```

Or run many at once:

```bash
docker compose up --scale producer=3
```

---

## ⚙️ Configuration

### Producer (`config.py`)
```python
BROKER_URL = "http://broker:5000"
TOPICS = ["temperature", "humidity", "pressure"]
INTERVAL_SECONDS = 2
```

---

## 🧑‍💻 Author

**LUI5DA**  
Systems Engineering Student at Universidad Nacional de Costa Rica  
> Exploring distributed systems, microservices, and Go one message at a time.