#!/usr/bin/env python3

import requests
import time

#Global Variables
api_key = "API_KEY"
chat_id = "YOUR_CHAT_ID"
bot_token = "YOUR_BOT_TOKEN_GOES_HERE"
threshold = 30000 #Immediate Price Alert if drops below this
time_interval = 5 * 60
print('Running..')
#Function to fetch BTC Price
def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY' : api_key
     }

     #Making a request to CoinMarketCap API
    response = requests.get(url, headers=headers)
    response_json = response.json()
    #The data the API return may vary in structure from time to time. If the above code doesn't get you the bitcoin price, then try to find where is bitcoin price in the response_json variable by printing the value in it and changing the last two lines according to that.

    btc = response_json['data'][0]
    btc_price = btc['quote']['USD']['price']
    #print(btc_price)
    return btc_price

#Function to send message in telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    #send the message
    requests.get(url)

#Main Function
def main():
    price_list = []

    #Infinite Loop
    while True:
        price = get_btc_price()
        price_list.append(price)

        #if price falls below threshold, immediate alert!
        if price < threshold:
            send_message(chat_id=chat_id, msg =f'BTC Price Drop Alert: {price}')

        #send past 5 prices
        if len(price_list) >= 5:
            send_message(chat_id=chat_id, msg = f'Last 5 BTC Prices:\n {price_list}')
            price_list = [] #empty the price list

        time.sleep(time_interval) #fetch the price every five minutes

#Just Activating main function
if __name__ == "__main__":
    main()
