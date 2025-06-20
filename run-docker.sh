#!/bin/bash
docker run --rm -it \
--name ubuntu-22 \
--network host \
-v /home:/home \
-w $(realpath .) \
ubuntu:22.04
