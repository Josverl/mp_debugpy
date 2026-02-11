#!/bin/bash

CONTAINER_NAME=${1:-micropython/debugpy:latest}
docker run -it --rm -p 5678:5678 \
    -v ./src:/usr/micropython \
    -v ./launcher:/usr/lib/micropython \
    -v ./micropython-lib/python-ecosys/debugpy:/root/.micropython/lib \
    "$CONTAINER_NAME" \
    -m mpy_launch_debugpy_unix run_pystone main