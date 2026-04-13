#! /bin/bash

# This is a minimal command to deploy Docassemble from Docker
# From: https://docassemble.org/docs/installation.html#docker
# The port mappings are to help avoid port collisions in deployment
# These mappings may need changing depending on what ports may already be in use

docker run -d \
    --name cls-docassemble \
    --env CONTAINERROLE=web \
    -p 8080:80 \
    --restart always \
    --stop-timeout 600 \
    jhpyle/docassemble
