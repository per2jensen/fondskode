import argparse
import requests
import sys
import pandas as pd

"""
Argparse webpages:
    https://realpython.com/python-command-line-arguments/
    https://www.golinuxcloud.com/python-argparse/
"""

# Realkredit lån, der kigges efter
FONDSKODE=952737
KURS=0.0


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

    if args.test:
        with open("../../test/Totalkredit-kurser.html") as f:
            html_text = f.read()
    else:
        totalkredit_url = 'https://netbank.totalkredit.dk/netbank/showStockExchangeInternal.do'
        html_text = requests.get(totalkredit_url).text


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
        #TODO insert into InsyncDB here
        sys.exit(0)
    else:
        print("Error: Fondskode '" + str(FONDSKODE) + "' blev ikke fundet")
        sys.ext(1)



