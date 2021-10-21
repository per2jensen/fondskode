import argparse
from influxdb import InfluxDBClient
import json
import requests
import sys
import pandas as pd

# Realkredit lån, der kigges efter
FONDSKODE=0 # beware: Pandas strips the leading "0"
TOTALKREDIT_URL=""
KURS=0.0

INFLUX_HOST="" # the hostname on the Docker network influx is deployed to
INFLUX_USER=''
INFLUX_PASS=''
INFLUX_DB=''

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Hent kursen for en fondskode hos TotalKredit."
    )
    parser.add_argument(
        "-c", "--configfile", dest="config", help="configfil placering", required=True
    )

    parser.add_argument(
        "-t", "--test", action="store_true", dest="test", help="brug kurserne fra fil i test biblioteket"
    )
    return parser

if __name__ == '__main__':
    
    parser = init_argparse()
    args = parser.parse_args()

    with open("config.json") as json_data_file:
        config = json.load(json_data_file)

    if args.test:
        with open("../../test/Totalkredit-kurser.html") as f:
            html_text = f.read()
    else:
        totalkredit_url = config["TOTALKREDIT_URL"]
        html_text = requests.get(totalkredit_url).text

    FONDSKODE   = int(config["FONDSKODE"])
    INFLUX_HOST = config["INFLUX_HOST"]
    INFLUX_USER = config["INFLUX_USER"]
    INFLUX_PASS = config["INFLUX_PASS"]
    INFLUX_DB   = config["INFLUX_DB"]

    df = pd.read_html(html_text)
    fondskode_fundet=False
    for tabel in df:
        for row in tabel.values:
            for el in row:
                if el == FONDSKODE:
                    KURS=row[4]/10000
                    fondskode_fundet = True
                    break
            if fondskode_fundet:
                break
        if fondskode_fundet:
            break

    if fondskode_fundet:
        print("Fondskode: " + str(FONDSKODE))
        print("Kurs: " + str(KURS))

        client = InfluxDBClient(host=INFLUX_HOST, port=8086, username=INFLUX_USER, password=INFLUX_PASS, database=INFLUX_DB)
        line = 'kurs,fondskode={0} value={1}'.format(FONDSKODE, KURS) 
        client.write([line], {'db': INFLUX_DB }, 204, 'line')
        client.close()
        sys.exit(0)
    else:
        print("Error: Fondskode '" + str(FONDSKODE) + "' blev ikke fundet")
        sys.exit(1)
