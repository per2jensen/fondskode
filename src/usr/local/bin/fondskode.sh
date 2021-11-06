#! /bin/bash

docker run \
  -e FONDSKODE='952737' \
  -e TOTALKREDIT_URL='https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do' \
  -e INFLUX_HOST='<host for influxdb>' \
  -e INFLUX_USER='<Influxdb user>' \
  -e INFLUX_PASS='<Influxdb user password>' \
  -e INFLUX_DB='<influxdb DB>' \
  --net <navn på docker netværk, hvis influxdb kører i en container> \
  --rm  \
  per2jensen/fondskode:latest

