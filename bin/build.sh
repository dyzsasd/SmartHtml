#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd )"

cd ${ROOT_DIR}

# Define your image name
IMAGE_NAME="smart-html"
TAG=$(git rev-parse --short HEAD)
PROJECT_ID="ethanwebcraft"

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME -t europe-docker.pkg.dev/ethanwebcraft/imf/$IMAGE_NAME:$TAG .
