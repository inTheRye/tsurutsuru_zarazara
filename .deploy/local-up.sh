#!/bin/bash
export NODE_ENV=local
export PORT=8080
cd ../.docker
docker-compose build
#docker-compose build --no-cache
docker-compose up

