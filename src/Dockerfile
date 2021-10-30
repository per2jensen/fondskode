FROM ubuntu:latest

RUN apt update && apt -y upgrade
RUN apt install -y python3.9
RUN apt install -y python3-pandas python3-requests python3-pip
RUN apt install python3-influxdb

RUN groupadd -r pj && useradd -r -s /bin/false -g pj pj

COPY python/kurs.py .

USER pj
CMD [ "python3", "kurs.py"]

