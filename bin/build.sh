#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd )"

cd ${ROOT_DIR}

# Define your image name
IMAGE_NAME="smart-html"
TAG="latest"
VERSION="0.1.0"
PROJECT_ID="ethanwebcraft"

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$TAG -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$VERSION .
