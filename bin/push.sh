IMAGE_NAME="smart-html"
TAG=$(git rev-parse --short HEAD)

docker push europe-docker.pkg.dev/ethanwebcraft/imf/$IMAGE_NAME:$TAG
