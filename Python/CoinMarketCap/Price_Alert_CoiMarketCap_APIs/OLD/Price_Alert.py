import json
import time
import pandas as pd
import pyttsx3
import requests


df = pd.read_csv('Coins.csv', usecols=['Symbol','Up','Down'])
df = df.to_json()
df = json.loads(df)

symbols = df['Symbol']
Up_limits = df['Up']
Down_limits = df['Down']

symbols = [symbols[x] for x in symbols]
Up_limits = [1000000 if Up_limits[x] is None else float(Up_limits[x]) for x in Up_limits]
Down_limits = [0 if Down_limits[x] is None else float(Down_limits[x]) for x in Down_limits]



current_price = [0] * len(symbols)
symbols_id = [0 for x in range(len(symbols))]

api = 'https://api.coinmarketcap.com/v2/listings/'
data = requests.get(api).json()['data']

for currency in data:
    if currency['name'] in symbols:
        symbols_id[symbols.index(currency['name'])] = currency['id']

api = 'https://api.coinmarketcap.com/v2/ticker/'

engine = pyttsx3.init()

def printing():
    while True:
        for index in range(len(symbols)):
            temp_api = api + str(symbols_id[index])
            data = requests.get(temp_api).json()
            current_price[index] = float(data['data']['quotes']['USD']['price'])

            if current_price[index] > Up_limits[index]:
                speak("%-10s price is %.2f" % (symbols[index],current_price[index]))
            if current_price[index] < Down_limits[index]:
                speak("%-10s price dropped %.2f" % (symbols[index],current_price[index]))

        time.sleep(300)

def speak(message):
    print(message)
    engine.say(message)
    engine.runAndWait()

printing()