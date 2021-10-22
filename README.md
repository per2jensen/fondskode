# Gem kursen på en Totalkredit obligationsserie

Jeg har et fastforrentet lån hos Totalkredit, og tænker det kunne være spændene at se kursudviklingen over tid.

# Min use case
Jeg har en Home Assistant instans med en InfluxDB time series database kørende, så det er naturlig at proppe nogle kursværdier ned i den.
InfluxDB bliver leveret med et pæresimpelt interface til at generere en graf med.


# Byg & test applikationen

scriptet test/build-run.sh gør følgende:

  - bygger applikationen
  - spinder en InfluxDB 1.8 container op
  - opretter en database
  - afvikler applikationen
  - checker at en kurs værdi er gemt i databasen
  - stopper DB

Det er nemt at sætte dine egne Influx connection parametre ind, kig i scriptet for at se hvordan.

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

