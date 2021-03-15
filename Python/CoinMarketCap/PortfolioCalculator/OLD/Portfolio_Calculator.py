import requests
from prettytable import PrettyTable

file = open('Portfolio.txt','r')

Symbols = []
Quantitys = []
Buy_prices = []

for line in file.readlines()[1:]:
    line = line.split(',')
    Symbols.append(line[0])
    Quantitys.append(float(line[1]))
    Buy_prices.append(float(line[2]))

api = 'https://api.coinmarketcap.com/v2/listings/'
data = requests.get(api).json()['data']

symbols_id = [0] * len(Symbols)


api = 'https://api.coinmarketcap.com/v2/ticker/'
table = PrettyTable()
table.field_names = ["Name","Quantity","Buy Price", 'Current Price ', "Profit %","Change 1h","Change 1d","Change 7d"]

for currency in data:
    if currency['name'] in Symbols:
        symbols_id[Symbols.index(currency['name'])] = currency['id']

def color(nr):
    if nr > 0:
        return ('\033[92m' + str(nr) + '\033[0m')
    else:
        return ('\033[91m' + str(nr) + '\033[0m')

current_value = 0
buy_value = 0

for i in range(len(Symbols)):
    temp_api = api + str(symbols_id[i])
    data = requests.get(temp_api).json()
    current_price = float(data['data']['quotes']['USD']['price'])
    change_1h = float(data['data']['quotes']['USD']['percent_change_1h'])
    change_1d = float(data['data']['quotes']['USD']['percent_change_24h'])
    change_7d = float(data['data']['quotes']['USD']['percent_change_7d'])

    profit = round(current_price/Buy_prices[i]*100-100,2)
    buy_value += Buy_prices[i] * Quantitys[i]
    current_value += current_price * Quantitys[i]
    table.add_row([Symbols[i],Quantitys[i],Buy_prices[i], current_price,color(profit),
                   color(change_1h),color(change_1d),color(change_7d)])

print(table)

total_profit = current_value / buy_value * 100 - 100
dolars = current_value - buy_value

print("Portfolio Value: %.2f   Total Profit %%: %.2f   Total Profit USD: %.2f" % (current_value,
                                                                               total_profit,dolars))