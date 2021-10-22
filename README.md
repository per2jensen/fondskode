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

## Systemd scheduling
Smid de to filer fra etc/systemd/system biblioteket over i /etc/systemd/system.
Dermed bliver programmet kørt en gang i døgnet, ind under midnat.

Kør derefter denne kommando
````
sudo systemctl daemon-reload 
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
# Links

  [Totalkredit siden med kurser](https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do)
  
  [Home Assistant](https://www.home-assistant.io/)
  
  [God side om Docker netværk](https://www.tutorialworks.com/container-networking/)
  
  [Pædagogisk side om "connection refused", indefra en container](https://pythonspeed.com/articles/docker-connection-refused/)

  [Hvis du vil ramme host localhost indefra en container....](https://www.cloudsavvyit.com/14114/how-to-connect-to-localhost-within-a-docker-container/)

  [Signing af docker images](https://betterprogramming.pub/docker-content-trust-security-digital-signatures-eeae9348140d)