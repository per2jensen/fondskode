#! /bin/bash

docker build --tag pj/fondskode  ../src
docker run --net hassio --rm  --name fondskode-getter -it pj/fondskode:latest
