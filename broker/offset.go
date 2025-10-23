// offset.go
package main

import (
    "fmt"
    "sync"
)

// Protect the offset map with a mutex for thread-safety
var mu sync.Mutex

// offsets[consumer_id:topic] = offset
var offsets = make(map[string]int)

// GetOffset returns the current offset for a given consumer/topic
func GetOffset(consumerID, topic string) int {
    mu.Lock()
    defer mu.Unlock()
    key := fmt.Sprintf("%s:%s", consumerID, topic)
    return offsets[key]
}

// IncrementOffset updates the offset after consuming a message
func IncrementOffset(consumerID, topic string) {
    mu.Lock()
    defer mu.Unlock()
    key := fmt.Sprintf("%s:%s", consumerID, topic)
    offsets[key]++
}
