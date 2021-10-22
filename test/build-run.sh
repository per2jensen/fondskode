#! /bin/bash

SCRIPTPATH=`realpath $0`
SCRIPTDIRPATH=`dirname $SCRIPTPATH`

docker build --tag per2jensen/fondskode  $SCRIPTDIRPATH/../src

echo Spin up InfluxDB 1.8
docker run -d \
  --rm \
  -e INFLUXDB_ADMIN_USER='CI_USER' \
  -e INFLUXDB_ADMIN_PASSWORD='thesecret' \
  -p 8086:8086 \
  influxdb:1.8

sleep 3
echo ping InfluxDB
curl -I -l http://localhost:8086/ping

echo create database
curl -I -G -X GET http://localhost:8086/query -u CI_USER:thesecret  --data-urlencode "q=CREATE DATABASE CI_DB"

echo run fondskode app to fecth kurs and store in InfluxDB
docker run \
  --add-host host.docker.internal:host-gateway \
  -e FONDSKODE='952737' \
  -e TOTALKREDIT_URL='https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do' \
  -e INFLUX_HOST='host.docker.internal' \
  -e INFLUX_USER='CI_USER' \
  -e INFLUX_PASS='thesecret' \
  -e INFLUX_DB='CI_DB' \
  --rm  -it per2jensen/fondskode:latest


echo Fetch the stored value from database
RESULT=$(curl -s -G "http://localhost:8086/query?pretty=true&db=CI_DB" -u CI_USER:thesecret  --data-urlencode "q=SELECT \"value\" FROM \"CI_DB\".\"autogen\".\"kurs\"")
echo $RESULT
echo ---- ============ ----
KURS=$(echo $RESULT| jq .results[].series[].values[0][1])
echo Kurs: $KURS
if [[ $KURS == "null" ]]; then
  exit 1
fi

docker stop $(docker ps |grep influxdb:1.8|cut -d" " -f1)
