import threading
import time
import requests


print("\nJust a moment...0%")
# You can also use APIs from CoinMarketCap
# Prices api
api = "https://api.binance.com/api/v1/ticker/24hr"
# Candlesticks api
api_klines_1m = "https://api.binance.com/api/v1/klines?interval=1m&limit=1000&symbol="
api_klines_1d = "https://api.binance.com/api/v1/klines?interval=1d&limit=1000&symbol="

symbols = []
indexes = []

data = requests.get(api).json()

minimum_volume = 100

# Calculate list of symbols
for currency in data:
    if "BTC" in currency['symbol'] and float(currency['quoteVolume']) > minimum_volume and len(symbols) < 10:
        symbols.append(currency['symbol'])
        indexes.append(data.index(currency))
prices_1m = [[]] * len(symbols)
prices_1d = [[] for each in range(len(symbols))]

# Get candlestick data
def kline_calculate(api):
    prices = [[] for each in range(len(symbols))]
    for symbol in symbols:
        temp_api = api + symbol
        candlesticks = requests.get(temp_api).json()
        for candle in candlesticks:
            prices[symbols.index(symbol)].append(float(candle[1]))
    return prices

prices_1m = kline_calculate(api_klines_1m)
print("\nJust a moment...50%")
prices_1d = kline_calculate(api_klines_1d)

# Declaration of list of parameters
current_price  = [0] * len(symbols)
current_score = [0] * len(symbols)
change_2m = [0] * len(symbols)
change_6h = [0] * len(symbols)
change_12h = [0] * len(symbols)
change_30d = [0 for x in range(len(symbols))]
change_1y = [0 for x in range(len(symbols))]
moving_average_30m = [0 for x in range(len(symbols))]
moving_average_30d = [0 for x in range(len(symbols))]

# Function for keeping up to date list of prices
def kline_continuum():
    seconds = 0

    while True:
        data = requests.get(api).json()
        i = 0

        for index in indexes:
            current_price[i] = float(data[index]['lastPrice'])
            if seconds % 60 == 0:
                prices_1m[i].append(current_price[i])
            i += 1
        time.sleep(5)
        seconds += 5

# Calculate percentage change between two prices
def calculate_change(curent_price, list, index):
    try:
        result = round(curent_price * 100 / list[index] - 100, 2)
    except:
        return 0

    return result

# Calculate score for all symbols
def calculate_score():
	
    # Calculate parameters for all symbols
    for symbol in range(len(symbols)):
        change_2m[symbol] = calculate_change(current_price[symbol],prices_1m[symbol], -2)
        change_6h[symbol] = calculate_change(current_price[symbol],prices_1m[symbol], -360)
        change_12h[symbol] = calculate_change(current_price[symbol],prices_1m[symbol], -720)
        change_30d[symbol] = calculate_change(current_price[symbol],prices_1d[symbol], -30)
        change_1y[symbol] = calculate_change(current_price[symbol],prices_1d[symbol], -365)

        #Calculate moving averages for 30 minute and 30 days
        average_30m = sum(prices_1m[symbol][-30:])/30
        moving_average_30m[symbol] = round(current_price[symbol] * 100 / average_30m - 100, 2)
        average_30d = sum(prices_1d[symbol][-30:])/30
        moving_average_30d[symbol] = round(current_price[symbol] * 100 / average_30d - 100, 2)

	
    # Calculate score for all symbols
    for symbol in range(len(symbols)):
        score = 0
        a = change_2m[symbol]
        if a > 0 and a < 0.5:
            score += 1
        elif a >= 0.5 and a < 1:
            score += 1.25

        a = change_6h[symbol]
        if a > 0 and a < 0.5:
            score += 1
        elif a >= 0.5 and a < 1:
            score += 1.25

        a = change_12h[symbol]
        if a > 0 and a < 0.5:
            score += 1
        elif a >= 0.5:
            score += 1.25


        a = change_30d[symbol]
        if a > 0 and a < 10:
            score += 1
        elif a >= 10:
            score += 1.5


        a = change_1y[symbol]
        if a > 0 and a < 20:
            score += 1
        elif a >= 20:
            score += 1.5

        a = moving_average_30m[symbol]
        if a > 0 and a < 0.5:
            score += 1
        elif a >= 0.5 and a < 1:
            score += 1.25


        a = moving_average_30d[symbol]
        if a > 0 and a < 0.5:
            score += 1
        elif a >= 0.5:
            score += 1.25

        current_score[symbol] = score

# Print results
def print_results():
    sort_index = 0
    while True:
        calculate_score()

        # List of sort_by parameters
        toggle_sort =[current_score,  change_2m, change_6h, change_12h, change_30d,
                        change_1y, moving_average_30m, moving_average_30d]

        # Parameter to sort for
        sort_by = toggle_sort[sort_index % len(toggle_sort)]

        # Sort data for sort_by
        sorted_data = sorted(range(len(sort_by)), key=lambda k: sort_by[k])
        # Reverse sort data
        sorted_data.reverse()

        # Print sort_by indicator
        print('         ' + ('       ' * (sort_index % len(toggle_sort))) + '______')

        # Print header
        print('%8s %6s %6s %6s %6s %6s %6s %6s %6s' % ('Symbol', 'score', '2m_ch','6h_ch','12h_ch', '30d_ch', '1y_ch', '30m_MA', '30d_MA'))

        # Print data for top 10 cryptocurrencies
        for index in range(10):
            i = sorted_data[index]
            print('%8s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f' %
                  (symbols[i], current_score[i],  change_2m[i], change_6h[i], change_12h[i], change_30d[i],
                   change_1y[i], moving_average_30m[i], moving_average_30d[i]))

        sort_index += 1

        time.sleep(5)

# Starting threads - you can add others by inserting into list of threads
threads = [threading.Thread(target=kline_continuum),
           #threading.Thread(target=exemple_of_add_thread),
           threading.Thread(target=print_results)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]