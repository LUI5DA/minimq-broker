# broker/Dockerfile
FROM golang:1.24.4 as builder

WORKDIR /app
COPY . .

RUN go mod tidy
RUN go build -o broker main.go handlers.go storage.go offset.go

FROM debian:bookworm-slim

WORKDIR /app
COPY --from=builder /app/broker .

RUN mkdir -p /app/data

EXPOSE 5000

CMD ["./broker"]
