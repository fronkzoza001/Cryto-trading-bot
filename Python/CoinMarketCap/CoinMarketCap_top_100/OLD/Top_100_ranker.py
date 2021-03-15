import requests
from prettytable import PrettyTable
import os

listings_api = 'https://api.coinmarketcap.com/v2/listings/'
ticker_api = 'https://api.coinmarketcap.com/v2/ticker/?start='
listings_data = requests.get(listings_api).json()['data']

table = PrettyTable()
table.field_names = ['Index','Name','Symbol','Price','Volume','MarketCap','Change 1h','Change 24h','Change 7d']

def isNone(number):
    if number:
        return float(number)
    return 0

i = 1
nr_coins = 0
coins = []
while nr_coins < len(listings_data):

    temp_ticker_api = ticker_api + str(nr_coins)
    ticker_data = requests.get(temp_ticker_api).json()
    ticker_data = ticker_data['data']

    for coin in ticker_data:
        name = ticker_data[coin]['name']
        symbol = ticker_data[coin]['symbol']
        coin = ticker_data[coin]['quotes']['USD']

        coins.append([  i,
                        name,
                        symbol,
                        isNone(coin['price']),
                        isNone(coin['volume_24h']),
                        isNone(coin['market_cap']),
                        isNone(coin['percent_change_1h']),
                        isNone(coin['percent_change_24h']),
                        isNone(coin['percent_change_7d'])])

        i += 1
    nr_coins += 100

while True:
    number = 1
    print("Press:")
    for item in table.field_names:
        print(str(number)+ ". Sort by " + item)
        number += 1

    choice = input("Choose sort option: ")

    coins.sort(key=lambda x: x[int(choice)-1])
    coins.reverse()

    [table.add_row(coin) for coin in coins[:100]]

    os.system('cls')
    print(table)
    table.clear_rows()