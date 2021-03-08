import requests
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pandas import DataFrame
from dotenv import load_dotenv

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


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
        #print(response.status_code)

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

#CSV stuff:
df = DataFrame(records)

filePath = os.path.join(os.path.dirname(__file__), "..", "data", f"{selectedSymbol}_prices.csv")

df.to_csv(filePath, index=False)

#Console stuff:
maxHold = records[1]["high"]
minHold = records[1]["low"]
for day in records:
    if day["high"] > maxHold:
        maxHold = day["high"]
    if day["low"] < minHold:   
        minHold = day["low"]

lastClose = records[0]["close"]
lastDay = records[0]["date"]

print("-------------------------")
print(f"SELECTED SYMBOL: {selectedSymbol}")
print("-------------------------")
print(f"REQUEST AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')}")
print(f"LAST UPDATED: {refreshedDate}")
print("-------------------------")
print(f"LATEST DAY: {lastDay}")
print(f"LATEST CLOSE: {to_usd(lastClose)}")
print(f"RECENT HIGH: {to_usd(maxHold)}")
print(f"RECENT LOW: {to_usd(minHold)}")
print("-------------------------")
if(lastClose < 1.2*minHold and lastClose < (minHold + maxHold)/2):
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: Latest close is less than 20% more than recent min and less than average of recent min/max")
else:
    print("RECOMMENDATION: DON'T BUY!")
    print("RECOMMENDATION REASON: Latest close is over 20% more than recent min or not less than average of recent min/max")
print("-------------------------")
print(f"Writing {selectedSymbol} info to csv file found in data folder, and making chart of recent closing prices...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#graph stuff
df["date"] = pd.to_datetime(df["date"])
sorted_df = df.sort_values(by="date")

sns.lineplot(data=df,x="date",y="close")

plt.title(f"Recent closing prices for {selectedSymbol}")
plt.show()