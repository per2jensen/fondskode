#! /bin/bash

docker build --tag pj/fondskode -f ../src/Dockerfile
docker run --net hassio --rm  --name fondskode-getter -it pj/fondskode:latest
