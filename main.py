from twilio.rest import Client

import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API = "ZMM5G03EFI7BJKTL"
NEW_API = "b275d7d8ccba420c8e4412793efdf03f"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": ALPHA_API
}
res = requests.get(STOCK_ENDPOINT, params=stock_params)
# print(res.json())
data = res.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]
print(yesterday_closing_price)

# TODO 2. - Get the day before yesterday's closing stock price
# day_before_yesterday_data =data_list[1]
day_before_yesterday_closing_price = data_list[1]["4. close"]
print(day_before_yesterday_closing_price)
# - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint:
# https://www.w3schools.com/python/ref_func_abs.asp
positive_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if positive_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(positive_difference)

# - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent =abs( (positive_difference / float(yesterday_closing_price)) * 100)
print(diff_percent)
up_down = None
# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 3:
        news_params={
            "apiKey": NEW_API,
            "qInTitle":COMPANY_NAME,
        }
        news_response=requests.get(NEWS_ENDPOINT,params=news_params)
        articles=news_response.json()["articles"]
        three_articles= articles[:3]
        print(three_articles)

        formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
        print(formatted_articles)
        # Send each article as a separate message via Twilio.
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        # TODO 8. - Send each article as a separate message via Twilio.
        for article in formatted_articles:
            message = client.messages.create(
                body=article,
                from_=VIRTUAL_TWILIO_NUMBER,
                to=VERIFIED_NUMBER
            )

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
