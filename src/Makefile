HELP_FORMAT = "\033[36m%-20s\033[0m %s\n"

IMAGE_NAME = unigram-payment_telegram-bot:${VERSION}
CONTAINER_NAME = unigram-payment_telegram-bot_container

PORT = 5000
VERSION = 1.0.4

.PHONY: help build run run-detached stop restart clear logs logs-realtime

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true

restart: clean run

clean: stop
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME)

logs:
	docker logs -f $(CONTAINER_NAME)

help:
	@echo "Available commands:"
	@printf $(HELP_FORMAT) "build" "Build the Docker image"
	@printf $(HELP_FORMAT) "run" "Start the Docker container"
	@printf $(HELP_FORMAT) "stop" "Stopping the Docker container."
	@printf $(HELP_FORMAT) "restart" "Restart the Docker container"
	@printf $(HELP_FORMAT) "logs" "View the Docker container logs"
	@printf $(HELP_FORMAT) "clean" "Deleting the Docker image"