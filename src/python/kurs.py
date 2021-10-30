import argparse
from influxdb import InfluxDBClient
import os
import requests
import sys
import pandas as pd

KURS=0.0

# Miljøvariabler givet til docker container
FONDSKODE=0 # beware: Pandas strips the leading "0"
TOTALKREDIT_URL=""
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
        "-t", "--test", action="store_true", dest="test", help="brug kurserne fra fil i test biblioteket"
    )
    return parser

if __name__ == '__main__':
    
    parser = init_argparse()
    args = parser.parse_args()

    FONDSKODE       = int(os.environ["FONDSKODE"])
    TOTALKREDIT_URL = os.environ["TOTALKREDIT_URL"]
    INFLUX_HOST     = os.environ["INFLUX_HOST"]
    INFLUX_USER     = os.environ["INFLUX_USER"]
    INFLUX_PASS     = os.environ["INFLUX_PASS"]
    INFLUX_DB       = os.environ["INFLUX_DB"]

    if args.test:
        with open("../../test/Totalkredit-kurser.html") as f:
            html_text = f.read()
    else:
        html_text = requests.get(TOTALKREDIT_URL).text

    df = pd.read_html(html_text)
    fondskode_fundet=False
    for tabel in df:
        for row in tabel.values:
            for el in row:
                try:
                    if int(el) == FONDSKODE:
                        KURS=row[4]/10000
                        fondskode_fundet = True
                        break
                except:
                    pass
            if fondskode_fundet:
                break
        if fondskode_fundet:
            break

    if fondskode_fundet:
        print("Fondskode: '{0}'".format(FONDSKODE))
        print("Kurs: {0}".format(KURS))

        client = InfluxDBClient(host=INFLUX_HOST, port=8086, username=INFLUX_USER, password=INFLUX_PASS, database=INFLUX_DB)
        line = 'kurs,fondskode={0} value={1}'.format(str(FONDSKODE), KURS)
        client.write([line], {'db': INFLUX_DB }, 204, 'line')
        client.close()
        sys.exit(0)
    else:
        print("Error: Fondskode '{0}' blev ikke fundet".format(str(FONDSKODE)))
        sys.exit(1)
