# ActiveMQ Artemis Mock Server

A mock server for developing and testing interactions with ActiveMQ Artemis queues.

## Quick Start

```bash
make start
```

- **Web Console**: http://localhost:8161
- Login: `admin`
- Password: `admin`

- `request.queue` - incoming requests, where you can connect to your system and send any request
- `response.queue` - outgoing responses - simulates the remote system and its response to your request

Responses are also stored in the local `answers/` directory, so they can be viewed after
consumption by your system.

## Templates

Request-response pairs are defined in the requests/response directories.

Add XML files to:
- `templates/requests/` - requests
- `templates/responses/` - corresponding responses (with the same name)

The listener will automatically pick up the new templates after restart (make restart-listener).

## Commands

A Makefile has been created for convenience. Basic commands:

- `make start` - Start the server
- `make stop` - Stop the server
- `make restart` - Restart
- `make restart-listener` - Restart the Listener
- `make reset` - Remove containers and rebuild
- `make test-request` - Generate 3 requests (1, 2, and the failed one) and send them to the queue
- `make logs` - Show logs
- `make logs-mock` - Show Artemis logs
- `make logs-listener` - Show Listener logs (can be run in one console and, for example, a test in another)
- `make clean` - Delete everything
- `make view-responses` - Message statistics in the response queue
  ```text
  Connection brokerURL = tcp://localhost:61616
  |NAME |ADDRESS |CONSUMER|MESSAGE|MESSAGES|DELIVERING|MESSAGES|SCHEDULED|ROUTING|INTERNAL|
  | | | COUNT | COUNT | ADDED | COUNT | ACKED | COUNT | TYPE | |
  |/queue/response.queue|/queue/response.queue| 0 | 6 | 12 | 0 | 0 | 0 | ANYCAST| false |
  d
  ```
- `make clean-responses` - Delete response files and clear the response queue