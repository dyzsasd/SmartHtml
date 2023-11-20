#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd )"

cd ${ROOT_DIR}

# Define your image name
IMAGE_NAME="smart-html-snapshot"

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed, exiting."
    exit 1
fi

# Run the Docker container
echo "Running Docker container..."
docker run -p 5000:5000 -v ${ROOT_DIR}:/usr/src/app $IMAGE_NAME
