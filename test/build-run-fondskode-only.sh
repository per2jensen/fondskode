#! /bin/bash

#
#  This script just runs fondskode, it fails on the InfluxDB insert
#

SCRIPTPATH=`realpath $0`
SCRIPTDIRPATH=`dirname $SCRIPTPATH`

docker build --tag per2jensen/fondskode  $SCRIPTDIRPATH/../src

echo run fondskode app to fecth kurs
docker run \
  --add-host host.docker.internal:host-gateway \
  -e FONDSKODE='952737' \
  -e TOTALKREDIT_URL='https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do' \
  -e INFLUX_HOST='host.docker.internal' \
  -e INFLUX_USER='DUMMY' \
  -e INFLUX_PASS='DUMMY' \
  -e INFLUX_DB='DUMMY' \
  -e DB_INSERT='FALSE' \
  --rm  -it per2jensen/fondskode:latest
