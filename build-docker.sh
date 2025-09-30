#!/bin/bash

docker rm -f vulnerable-flask
docker build -t vulnerable-flask .
docker run -p 5000:5000 --rm --name vulnerable-flask vulnerable-flask
