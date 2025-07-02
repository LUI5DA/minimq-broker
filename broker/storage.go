// storage.go
package main

import (
    "fmt"
    "os"
    "sync"
)

// One mutex per topic
var topicLocks = make(map[string]*sync.Mutex)
var topicLockMu sync.Mutex  // Global lock for protecting the map


func getTopicLock(topic string) *sync.Mutex {
    topicLockMu.Lock()
    defer topicLockMu.Unlock()

    // If no lock for this topic yet, create one
    if _, exists := topicLocks[topic]; !exists {
        topicLocks[topic] = &sync.Mutex{}
    }

    return topicLocks[topic]
}


// Save a message in a log file
func appendMessageToFile(topic, message string) error {
    lock := getTopicLock(topic)
    lock.Lock()
    defer lock.Unlock()

    path := fmt.Sprintf("data/%s.log", topic)

    f, err := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return err
    }
    defer f.Close()

    _, err = f.WriteString(message + "\n")
    return err
}



// Read the message at the given offset (0 = first message)
func readMessageAtOffset(topic string, offset int) (string, error) {
    path := fmt.Sprintf("data/%s.log", topic)

    data, err := os.ReadFile(path)
    if err != nil {
        return "", err
    }

    lines := splitLines(string(data))

    if offset >= len(lines) {
        return "", nil // No new message yet
    }

    return lines[offset], nil
}

// Custom line splitter to handle cross-platform line endings
func splitLines(data string) []string {
    var lines []string
    start := 0
    for i, c := range data {
        if c == '\n' {
            lines = append(lines, data[start:i])
            start = i + 1
        }
    }
    // Add last line if no newline at end
    if start < len(data) {
        lines = append(lines, data[start:])
    }
    return lines
}
