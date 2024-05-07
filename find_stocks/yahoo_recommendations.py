# Import dependencies
import requests
import pandas as pd
import datetime
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
sys.path.append(os.path.dirname(os.getcwd()))
import utils.tickers as ti

# Define today's date
today = datetime.date.today()

# Prepare ticker symbols
tickers = ti.tickers_sp500()
tickers = [ticker.replace(".", "-") for ticker in tickers]

# Initialize list for recommendations
recommendations = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
# Process each ticker
ticker = 'AAPL'
for ticker in tickers:
    try:
        url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=financialData'
        response = requests.get(url, headers=headers)
        if response.ok:
            result = response.json()['quoteSummary']['result'][0]
            recommendation = result['financialData']['recommendationMean']['fmt']
        else:
            # print("No ok")
            recommendation = None  # None for failed requests
    except Exception as e:
        print(e)
        recommendation = None  # None for parsing failures

    recommendations.append(recommendation)
    time.sleep(1.5)  # Delay to avoid overloading server

    print(f"{ticker} has an average recommendation of: {recommendation}")

# Load existing data and update with new recommendations
try:
    df = pd.read_csv('recommendation-values.csv', index_col='Company')
except FileNotFoundError:
    df = pd.DataFrame(index=tickers)

df[today] = recommendations
df.to_csv('recommendation-values.csv')
print(df)