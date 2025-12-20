.PHONY: help build stop clean logs shell test push pull rebuild

# Variables
IMAGE_NAME := localhost:5000/personal-site
IMAGE_TAG := latest
FULL_IMAGE := $(IMAGE_NAME):$(IMAGE_TAG)
COMPOSE_FILE := docker-compose.yml
APP_DIR := app

# Default target
help:
	@echo "Available targets:"
	@echo "  make build       - Build the Docker image"
	@echo "  make stop        - Stop the running container"
	@echo "  make logs        - Show container logs"
	@echo "  make shell       - Open a shell in the running container"
	@echo "  make clean       - Remove containers and images"
	@echo "  make rebuild     - Rebuild and restart the container"
	@echo "  make test        - Test the build process"
	@echo "  make push        - Push image to registry"
	@echo "  make pull        - Pull image from registry"

# Process logo (make white background transparent)
logo:
	@echo "Processing logo..."
	cd $(APP_DIR) && python3 make_logo_transparent.py || echo "Logo processing skipped - ensure logo004.png exists in app/"

# Build the Docker image
build: logo
	@echo "Building Docker image: $(FULL_IMAGE)"
	cd $(APP_DIR) && docker build -t $(FULL_IMAGE) .

# Build using docker-compose
build-compose:
	@echo "Building with docker-compose..."
	docker-compose -f $(COMPOSE_FILE) build

# Stop the container
stop:
	@echo "Stopping container..."
	docker-compose -f $(COMPOSE_FILE) stop

# Stop and remove containers
down:
	@echo "Stopping and removing containers..."
	docker-compose -f $(COMPOSE_FILE) down

# Show logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Open a shell in the running container
shell:
	@echo "Opening shell in container..."
	docker-compose -f $(COMPOSE_FILE) exec personal-site sh

# Clean up: remove containers, images, and volumes
clean:
	@echo "Cleaning up containers and images..."
	docker-compose -f $(COMPOSE_FILE) down -v --rmi local
	@echo "Removing image $(FULL_IMAGE) if it exists..."
	-docker rmi $(FULL_IMAGE) 2>/dev/null || true

# Rebuild
rebuild: stop build
	@echo "Rebuild complete!"

# Test the build (dry run)
test:
	@echo "Testing build process..."
	cd $(APP_DIR) && docker build -t $(FULL_IMAGE)-test .
	@echo "Build test successful!"
	-docker rmi $(FULL_IMAGE)-test 2>/dev/null || true

# Push image to registry
push:
	@echo "Pushing image to registry..."
	docker push $(FULL_IMAGE)

# Pull image from registry
pull:
	@echo "Pulling image from registry..."
	docker pull $(FULL_IMAGE)


# Show container status
status:
	@echo "Container status:"
	docker-compose -f $(COMPOSE_FILE) ps

# Show container resource usage
stats:
	docker stats $$(docker-compose -f $(COMPOSE_FILE) ps -q)
