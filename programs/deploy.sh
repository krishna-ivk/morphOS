#!/bin/bash

echo "Deploying application..."

docker build -t app .
docker run -d -p 8080:8080 app
