// handlers.go
package main

import (
    "encoding/json"
    // "io/ioutil"
    "net/http"
    "log"
)

type Message struct {
    Topic   string `json:"topic"`
    Message string `json:"message"`
}

// /produce
func handleProduce(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var msg Message
    err := json.NewDecoder(r.Body).Decode(&msg)
    if err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    log.Printf("Received message on topic %s: %s", msg.Topic, msg.Message)

    err = appendMessageToFile(msg.Topic, msg.Message)
	if err != nil {
		log.Printf("Error writing to file: %v", err)
		http.Error(w, "Could not store message", http.StatusInternalServerError)
		return
	}


    w.WriteHeader(http.StatusCreated)
}

// handleConsume returns the next message for a consumer
func handleConsume(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    topic := r.URL.Query().Get("topic")
    consumerID := r.URL.Query().Get("consumer_id")

    if topic == "" || consumerID == "" {
        http.Error(w, "Missing topic or consumer_id", http.StatusBadRequest)
        return
    }

    offset := GetOffset(consumerID, topic)
    message, err := readMessageAtOffset(topic, offset)

    if err != nil {
        http.Error(w, "Failed to read message", http.StatusInternalServerError)
        return
    }

    if message == "" {
        w.WriteHeader(http.StatusNoContent) // No new messages
        return
    }

    // Advance the offset
    IncrementOffset(consumerID, topic)

    // Return the message as JSON
    response := map[string]interface{}{
        "message": message,
        "offset":  offset,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

