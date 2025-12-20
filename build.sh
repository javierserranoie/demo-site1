#!/bin/bash
# Build script for personal-site Docker image

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/app"

echo "Building Docker image from app/ directory..."
docker build -t localhost:5000/personal-site:latest .

echo "Build complete!"
