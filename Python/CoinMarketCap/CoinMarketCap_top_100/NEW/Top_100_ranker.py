import requests
from prettytable import PrettyTable
import os

listings_api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&limit=5000&cryptocurrency_type=tokens&convert=USD'


headers = {
  'content-type': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

listings_data = requests.get(listings_api,headers=headers).json()
listings_data = listings_data['data']

table = PrettyTable()
table.field_names = ['Index','Name','Symbol','Price','Volume','MarketCap','Change 1h','Change 24h','Change 7d']

def isNone(number):
    if number:
        return float(number)
    return 0

i = 1
nr_coins = 0
coins = []
for ticker_data in listings_data:

        name = ticker_data['name']
        symbol = ticker_data['symbol']
        coin = ticker_data['quote']['USD']

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