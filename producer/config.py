# config.py

#BROKER_URL = "http://localhost:5000/produce"  # or 'http://broker:5000' in Docker
BROKER_URL = "http://broker:5000"
TOPICS = ["temperature", "humidity", "pressure"]
INTERVAL_SECONDS = 2
