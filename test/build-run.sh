#! /bin/bash

#
#  Build a container using podman and execute it
#

podman build --tag ubuntu:fondskode -f ../test/Dockerfile
podman run -it ubuntu:fondskode
