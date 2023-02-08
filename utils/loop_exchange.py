import time
from collections import namedtuple
import requests
from testobot import check


def get_exchange_network():
    rate = namedtuple("Rate", "eur usd date")
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    except:
        print("Курс валют не получен")
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    print(f'usd {usd},eur {eur}')
    date = (data['Timestamp'].split('T'))
    return rate(eur=eur, usd=usd, date=date)

def save_exchange(xrate):
    usd = xrate.usd
    eur = xrate.eur
    date = xrate.date
    string =f"{usd}|{eur}|{date}"
    print("save new exchange:  ", string)
    with open('exchange.txt','w+') as file:
        file.write(string)
        file.close()


if __name__ == '__main__':
    while True:
        save_exchange(get_exchange_network())
        print("from exchange",check)
        time.sleep()

