import requests
from prettytable import PrettyTable

file = open('Portfolio.txt','r')

headers = {
  'content-type': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY',
}

Symbols = []
Quantitys = []
Buy_prices = []

for line in file.readlines()[1:]:
    line = line.split(',')
    Symbols.append(line[0])
    Quantitys.append(float(line[1]))
    Buy_prices.append(float(line[2]))

api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&limit=5000&convert=USD'
data = requests.get(api, headers=headers).json()['data']

symbols_id = [0] * len(Symbols)

table = PrettyTable()
table.field_names = ["Name","Quantity","Buy Price","Profit","Change 1h","Change 1d","Change 7d"]


for currency in data:
    if currency['name'] in Symbols:
        symbols_id[Symbols.index(currency['name'])] = currency['id']


def color(nr):
    if nr > 0:
        return ('\033[92m' + str(nr) + '\033[0m')+"%"
    else:
        return ('\033[91m' + str(nr) + '\033[0m')+"%"

current_value = 0
buy_value = 0
i = 0
for symbol in symbols_id:
    for coin in data:
        if(symbol == coin["id"]):
            current_price = float(coin['quote']['USD']['price'])
            change_1h = float(coin['quote']['USD']['percent_change_1h'])
            change_1d = float(coin['quote']['USD']['percent_change_24h'])
            change_7d = float(coin['quote']['USD']['percent_change_7d'])

            profit = round(current_price/Buy_prices[i]*100-100,2)
            buy_value += Buy_prices[i] * Quantitys[i]
            current_value += current_price * Quantitys[i]
            table.add_row([Symbols[i],Quantitys[i],Buy_prices[i],color(profit),
                           color(change_1h),color(change_1d),color(change_7d)])
            i += 1
            break

print(table)
total_profit = current_value / buy_value * 100 - 100
dolars = current_value - buy_value

print("Portfolio Value: %.2f   Total Profit: %.2f%%   Total Profit USD: %.2f" % (current_value,
                                                                               total_profit,dolars))