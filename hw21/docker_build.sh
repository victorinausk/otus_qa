#!/bin/bash

echo "building docker"

docker build --build-arg SSH_MASTER_USER=master --build-arg SSH_MASTER_PASS=master -t victorinausk/sftp:latest ./docker
docker push victorinausk/sftp:latest
