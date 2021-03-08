import requests
import os
import json
from pandas import DataFrame
from dotenv import load_dotenv


ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS, please set env var called 'ALPHAVANTAGE_API_KEY'")

bad = True

while bad:
    ticker = input("Please enter the ticker you are interested in: ")
    if any(char.isdigit() for char in ticker):
        print("Please do not include numbers. Try again.")
    elif any(not char.isalnum() for char in ticker):
        print("Please do not include symbols or spaces. Try again.")
    elif len(ticker) > 5:
        print("Please input a ticker that has 5 or less characters")
    else:
        ticker = ticker.upper()

        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHAVANTAGE_API_KEY}"

        response = requests.get(request_url)
        print(response.status_code)

        if "Error" in response.text:
            print(f"Error - Error with your ticker, make sure it's correct and please try again.")
        else:
            bad = False


parsed_response = json.loads(response.text)
#print(type(parsed_response))
#print(parsed_response.keys())
refreshedDate = parsed_response["Meta Data"]["3. Last Refreshed"]
selectedSymbol = parsed_response["Meta Data"]["2. Symbol"]
records = []
for date, daily_data in parsed_response["Time Series (Daily)"].items():
    record = {
        "date" : date,
        "open" : float(daily_data["1. open"]),
        "high" : float(daily_data["2. high"]),
        "low" : float(daily_data["3. low"]),
        "close" : float(daily_data["4. close"]),
        "volume" : int(daily_data["5. volume"])
    }
    records.append(record)



#print("-------------------------")
print(f"SELECTED SYMBOL: {selectedSymbol}")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: 2018-02-20 02:00pm")
print(f"LAST UPDATED: {refreshedDate}")
#print("-------------------------")
#print("LATEST DAY: 2018-02-20")
#print("LATEST CLOSE: $100,000.00")
#print("RECENT HIGH: $101,000.00")
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")