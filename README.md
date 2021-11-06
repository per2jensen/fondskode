# Gem kursen på en Totalkredit obligationsserie

Jeg har et fastforrentet lån hos Totalkredit, og tænker det kunne være spændene at se kursudviklingen over tid.

# Min use case
Jeg har en Home Assistant instans med en InfluxDB time series database kørende, så det er naturlig at proppe nogle kursværdier ned i den.
InfluxDB bliver leveret med et pæresimpelt interface til at generere en graf med.

# Byg & test applikationen

scriptet test/build-run.sh gør følgende:

  - bygger applikationen i et docker image
  - spinder en InfluxDB 1.8 container op
  - opretter en database
  - afvikler applikationen i en container (finder kursen og gemmer den)
  - checker at kurs værdien er gemt i databasen
  - stopper InfluxDB

Det er nemt at sætte dine egne Influx connection parametre ind, kig i scriptet for at se hvordan.
Vær opmærksom på, at du skal have [Docker](https://www.docker.com/) installeret.
Se og test scriptet på denne måde:

````
git clone https://github.com/per2jensen/fondskode.git
fondskode/test/build-run.sh
````

# Kør applikationen (uden byg)

Fondskode applikationen ligger på Docker Hub. Du kan se den køre på denne måde:

````
git clone https://github.com/per2jensen/fondskode.git
fondskode/test/run.sh
````
Vær opmærksom på, at du skal have [Docker](https://www.docker.com/) installeret.

# Kør applikationen og gem i en Home Assistant InfluxDB

  For at programmet kan forbinde til InfluxDB på Home Assistant docker netværket, skal du kende hostname.
  Det kan findes på denne måde:
  ````
  docker network ls
  ````
  
  som måske giver noget som dette:
  ````
  NETWORK ID     NAME      DRIVER    SCOPE
  ac10b63fd2a7   bridge    bridge    local
  292272e9dbc0   hassio    bridge    local
  4401ed03b0bc   host      host      local
  e6ac28b3b92b   none      null      local
  ````


  "hassio" er netværket som Home Assistant opretter (2021-10-30). Nu kan du finde hostnavnet på din InfluxDB container på denne måde:
  ````
  docker network inspect hassio|grep -i influxdb
    "Name": "addon_a0d7b954_influxdb"
  ````

  Navnet er således "addon_a0d7b954_influxdb". Det sætter du ind som miljø variabel i shell scriptet nedenfor:
  ````
    #! /bin/bash

    docker run \
    -e FONDSKODE='952737' \
    -e TOTALKREDIT_URL='https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do' \
    -e INFLUX_HOST='addon_a0d7b954_influxdb' \
    -e INFLUX_USER='<din influx user>' \
    -e INFLUX_PASS='<din influx users password' \
    -e INFLUX_DB='<fondskode databasen>' \
    --net hassio \
    --rm  -it per2jensen/fondskode:latest
  ````


# Systemd scheduling
Smid de to filer fra etc/systemd/system biblioteket over i /etc/systemd/system.
Dermed bliver programmet kørt en gang i døgnet, ind under midnat.

Kør derefter denne kommando
````
sudo systemctl enable fondskode-getter.timer
sudo systemctl start fondskode-getter.timer
 
````

Check at timeren er sat og er klar
````
systemctl list-timers |grep -i fondskode
````


# Docker Hub

Der ligger et færdigbygget image på [Docker Hub)(https://hub.docker.com/repository/registry-1.docker.io/per2jensen/fondskode)

## Offentlig nøgle
Images på Docker Hub er signeret af mig.

Den offentlige nøgle er denne:
````
-----BEGIN PUBLIC KEY-----
role: fondskode

MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEy73oXfqT1Sw/yEymBvMoGZNi7YA2
DLGahWTwEMrCa7zdUSXySXm+6e2KLgtM2Xv+i5YzxZ3GGJJZHVPnu139Uw==
-----END PUBLIC KEY-----
````

## Docker trust
Man kan se hvilke nøgler der kan signe docker images i per2jensen/fondskode repoet:
````
~$ docker trust inspect --pretty per2jensen/fondskode:latest

Signatures for per2jensen/fondskode:latest

SIGNED TAG   DIGEST                                                             SIGNERS
latest       847278dd7bf3c3d94d63403ff0e1ed17f0cc2119f0a5ea5894c19b92f5ac4661   fondskode

List of signers and their keys for per2jensen/fondskode:latest

SIGNER      KEYS
fondskode   890fff0490ab

Administrative keys for per2jensen/fondskode:latest

  Repository Key:	5f35ea18dde68e1777d3d4f25b2d4b28151c8e0ea3edb9ee27f2419ed37136d2
  Root Key:	25961d155ac858734487619894dd04e666d436e35bc327f1f1fd30243f415c9f

````


# Links

  [Totalkredit siden med kurser](https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do)
  
  [Home Assistant](https://www.home-assistant.io/)
  
  [God side om Docker netværk](https://www.tutorialworks.com/container-networking/)
  
  [Pædagogisk side om "connection refused", indefra en container](https://pythonspeed.com/articles/docker-connection-refused/)

  [Hvis du vil ramme host localhost indefra en container....](https://www.cloudsavvyit.com/14114/how-to-connect-to-localhost-within-a-docker-container/)

  [Signing af docker images](https://betterprogramming.pub/docker-content-trust-security-digital-signatures-eeae9348140d)
  
  [Docker trust](https://docs.docker.com/engine/security/trust/)
