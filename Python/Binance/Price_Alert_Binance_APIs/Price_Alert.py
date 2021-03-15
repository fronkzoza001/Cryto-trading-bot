import time
import pandas as pd
import json
import requests
import pyttsx3

df = pd.read_csv("Coins.csv",
                 usecols= ["Symbol","Up","Down"])

df1 = df.to_json()
df_json = json.loads(df1)

symbols = df_json['Symbol']
Up_limits = df_json['Up']
Down_limits = df_json['Down']


symbols = [symbols[x] for x in symbols]

#Up_limits = [float(Up_limits[x]) for x in Up_limits]
Up_limits = [100000 if Up_limits[x] is None else float(Up_limits[x]) for x in Up_limits]
Down_limits = [0 if Down_limits[x] is None else float(Down_limits[x]) for x in Down_limits]

api = "https://api.coinmarketcap.com/v2/listings/"
data = requests.get(api).json()['data']

api_indexes = [0 for x in range(len(symbols))]
current_price = [0 for x in range(len(symbols))]
for currency in data:
    if currency['name'] in symbols:
        api_indexes[symbols.index(currency["name"])] = currency['id']

api = "https://api.coinmarketcap.com/v2/ticker/"


engine = pyttsx3.init()


def printing():
    while True:
        for index in range(len(symbols)):
            temp_api = api + str(api_indexes[index])
            data = requests.get(temp_api).json()
            current_price[index] = float(data['data']['quotes']['USD']['price'])

            if current_price[index] > Up_limits[index]:
                speak("%-10s price is %.2f" % (symbols[index],current_price[index]))
            if current_price[index] < Down_limits[index]:
                speak("%-10s price dropped to %.2f" % (symbols[index],current_price[index]))
        time.sleep(10)

def speak(message):
    print(message)
    engine.say(message)
    engine.runAndWait()

printing()