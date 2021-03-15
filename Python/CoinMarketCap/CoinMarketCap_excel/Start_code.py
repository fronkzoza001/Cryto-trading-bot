import requests
from prettytable import PrettyTable

listings_api = 'https://api.coinmarketcap.com/v2/listings/'
ticker_api = 'https://api.coinmarketcap.com/v2/ticker/?start='
listings_data = requests.get(listings_api).json()['data']

table = PrettyTable()
table.field_names = ['Name','Symbol','Price','Volume','MarketCap','Change 1h','Change 24h','Change 7d']

nr_coins = 0

while nr_coins < len(listings_data):

    temp_ticker_api = ticker_api + str(nr_coins)
    ticker_data = requests.get(temp_ticker_api).json()
    ticker_data = ticker_data['data']

    for coin in ticker_data:
        name = ticker_data[coin]['name']
        symbol = ticker_data[coin]['symbol']
        coin = ticker_data[coin]['quotes']['USD']

        table.add_row([ name,
                        symbol,
                        coin['price'],
                        coin['volume_24h'],
                        coin['market_cap'],
                        coin['percent_change_1h'],
                        coin['percent_change_24h'],
                        coin['percent_change_7d']])

    nr_coins += 100

print(table)