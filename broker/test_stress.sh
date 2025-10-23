#!/bin/bash

# Number of messages to send
COUNT=1000

# Topic to produce to
TOPIC="temperature"

# URL of the broker
BROKER_URL="http://localhost:5000/produce"

echo "Sending $COUNT messages to topic '$TOPIC'..."

for i in $(seq 1 $COUNT); do
  VALUE=$((20 + RANDOM % 10)) # Random temperature between 20 and 29
  curl -s -X POST "$BROKER_URL" \
    -H "Content-Type: application/json" \
    -d "{\"topic\": \"$TOPIC\", \"message\": \"$VALUE\"}" &
done

# Wait for all background jobs to finish
wait

echo "Done sending $COUNT messages."
