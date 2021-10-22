#! /bin/bash

docker build --tag per2jensen/fondskode  ../src
docker run --net hassio --rm  --name fondskode-getter -it per2jensen/fondskode:latest
