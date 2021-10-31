FROM ubuntu:latest
WORKDIR /usr/local/fondskode

# set TZ to Copenhagen  - avoid tzdata update requiring user interaction
RUN echo 'tzdata tzdata/Areas select Europe' | debconf-set-selections  && \
    echo 'tzdata tzdata/Zones/Europe select Copenhagen' | debconf-set-selections && \
    apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y tzdata

RUN apt-get install -y \
    python3.9 \
    python3-pandas \
    python3-requests \
    python3-pip \
    python3-influxdb

RUN groupadd -r pj && useradd -r -s /bin/false -g pj pj

COPY python/kurs.py .

USER pj
CMD [ "python3", "kurs.py"]

