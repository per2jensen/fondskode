# Gem kursen på en Totalkredit obligationsserie

Jeg har et fastforrentet lån hos Totalkredit, og tænker det kunne være spændene at se kursudviklingen over tid.

# Min use case
Jeg har en Home Assistant instans med en InfluxDB time series database kørende, så det er naturlig at proppe nogle kursværdier ned i den.
InfluxDB bliver leveret med et pæresimpelt interface til at generere en graf med.

# Installation

Jeg forudsætter du har en InfluxDB kørende i en Docker container

## InfluxDB

Check om der er forbindelse fra din host
````
curl -sl -I localhost:8086/ping
````

Opret en database (jeg antager at brugeren er oprettet)
````
curl -I -G -X GET http://localhost:8086/query -u <db brugernavn>:<db bruger password>  --data-urlencode "q=CREATE DATABASE fondskode"
````

## Byg en docker container
Clone dette repo til din maskine

"cd" til <repoet>/src/python. Kopier config.json.template --> config.json og ret de nødvendige parametre til dit brug.
  
"cd .." til <repoet>/src

byg et Docker image
````
docker build -t pj/fondskode .
````

Kør docker containeren (--net hassio, fordi min InfluxDB er installeret via Home Assistant)
````
docker run --net hassio --rm --name fondskode-getter -it pj/fondskode:latest
````

## Systemd 
Smid de to filer fra etc/systemd/system biblioteket over i /etc/systemd/system.
Dermed bliver programmet kørt en gang i døgnet, ind under midnat.

Kør derefter denne kommando
````
sudo systemctl daemon-reload 
````
# Links

  [Totalkredit siden med kurser](https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do)
  
  [Home Assistant](https://www.home-assistant.io/)
  
  [God side om Docker netværk](https://www.tutorialworks.com/container-networking/)
  
  [Pædagogisk side om "connection refused", indefra en container](https://pythonspeed.com/articles/docker-connection-refused/)

  [Hvis du vil ramme host localhost indefra en container....](https://www.cloudsavvyit.com/14114/how-to-connect-to-localhost-within-a-docker-container/)

