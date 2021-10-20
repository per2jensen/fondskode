FROM ubuntu:latest

RUN apt update
RUN apt install -y python3.9
RUN apt install -y python3-pandas python3-requests python3-pip
RUN apt install python3-influxdb

COPY python/kurs.py .
COPY python/config.json .
CMD [ "python3", "kurs.py", "-c", "config.json"]

