// main.go
package main

import (
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/produce", handleProduce)
    http.HandleFunc("/consume", handleConsume)
    http.HandleFunc("/nodes", handleNodes)


    log.Println("Broker running on port 5000...")
    if err := http.ListenAndServe(":5000", nil); err != nil {
        log.Fatalf("Server failed: %s", err)
    }
}
