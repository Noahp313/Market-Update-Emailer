from decimal import Decimal
from io import StringIO
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# for .env
load_dotenv()


def indicies_text(): # for getting text of indicies changing
    indicies = ["^GSPC", "^DJI", "^IXIC", "^VIX", "GLD", "DX-Y.NYB"] #sp500, djia, nasdaq, vix, gold, dollar basket

    data = yf.download(indicies, period="2d", group_by="ticker", auto_adjust=True, threads=True)

    changeData = []
    for index in indicies: # appends each index and its change to list
        close_today = data[index]["Close"].iloc[-1]
        close_yesterday = data[index]["Close"].iloc[-2]
        change = (close_today - close_yesterday) / close_yesterday * 100
        changeData.append([index, change])

    changeDataDF = pd.DataFrame(changeData, columns=["Ticker", "Percent Change"]) # creates DF

    # neatly formats results
    text = "Indicies: \n"
    for _, index in changeDataDF.iterrows():
        text += yf.Ticker(index["Ticker"]).info["longName"] + " - CLOSE: " + str(data[index["Ticker"]]["Close"].iloc[-1]) + " (" + str(round(index["Percent Change"], 2)) + "%)\n"

    text += "\n"
    return text

def gain_and_lose_text(): # for getting gainers and losers
    # wikipedia query
    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",  headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text

    sp500tickers = []

    sizeList = 10

    for ticker in pd.read_html(StringIO(response))[0]["Symbol"]: # for each ticker from wikipedia list
        ticker = ticker.replace(".", "-") # fixes ticker
        sp500tickers.append(ticker) # added to list

    data = yf.download(sp500tickers, period="2d", group_by="ticker", auto_adjust=True, threads=True) # downloads yf info

    changeData = []

    for company in sp500tickers: # for each company, calculate daily change
        close_today = data[company]["Close"].iloc[-1]
        close_yesterday = data[company]["Close"].iloc[-2]
        change = (close_today - close_yesterday) / close_yesterday * 100
        changeData.append([company, change])

    changeDataDF = pd.DataFrame(changeData, columns=["Ticker", "Percent Change"]) # create DF with results

    # gathers 10 most extreme gainers and 10 most extreme losers
    gainers = changeDataDF.sort_values("Percent Change", ascending=False).head(sizeList)
    losers = changeDataDF.sort_values("Percent Change", ascending=True).head(sizeList)

    # neatly displays output
    text = "Gainers: \n"
    for _, gainerStock in gainers.iterrows():
        text += yf.Ticker(gainerStock["Ticker"]).info["longName"] + " (" + gainerStock["Ticker"] + ") -> " + str(round(gainerStock["Percent Change"], 2)) + "%\n"

    text += "\nLosers: \n"
    for _, loserStock in losers.iterrows():
        text += yf.Ticker(loserStock["Ticker"]).info["longName"] + " (" + loserStock["Ticker"] + ") -> " + str(round(loserStock["Percent Change"], 2)) + "%\n"

    text += "\n"

    return text

def earnings_text(): # for getting earnings day

    # use Earnings API
    earnings_api_key = os.getenv("EARNINGS_KEY")

    # access proper dates
    yesterday_date = (datetime.today() + pd.Timedelta(days=-1)).strftime("%Y-%m-%d")
    today_date = datetime.today().strftime("%Y-%m-%d")
    tomorrow_date = (datetime.today() + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    
    # API query
    yesterday_earnings = requests.get("https://api.earningsapi.com/v1/calendar/" + yesterday_date + "?apikey=" + earnings_api_key).json()
    today_earnings = requests.get("https://api.earningsapi.com/v1/calendar/" + today_date + "?apikey=" + earnings_api_key).json()
    tomorrow_earnings = requests.get("https://api.earningsapi.com/v1/calendar/" + tomorrow_date + "?apikey=" + earnings_api_key).json()

    upcoming_earnings = []
    past_earnings = []

    # get each company's market cap, and check if it is greater than 75 billion
    for day in [yesterday_earnings, today_earnings, tomorrow_earnings]:
        for timing in [day["pre"], day["after"], day["notSupplied"]]:
                for company in timing:
                    try: 
                        marketCap = yf.Ticker(company["symbol"]).fast_info["marketCap"]
                        if marketCap:
                            decimalMarketCap = Decimal(str(marketCap))
                            if not company["eps"]: # if it is upcoming
                                if decimalMarketCap > 75000000000:
                                    date = "Unsure"

                                    # finds correct date
                                    if day == tomorrow_earnings:
                                        date = str(tomorrow_date)
                                    elif day == yesterday_earnings:
                                        date = str(yesterday_date)
                                    elif day == today_earnings:
                                        date = str(today_date)
             
                                    # appends all data to 2D list
                                    upcoming_earnings.append([company["symbol"], company["name"], date])
                            else: # if it is past
                                if decimalMarketCap > 75000000000:
                                    epsFixed = None
                                    epsEstimateFixed = None
                                    revenueFixed = None
                                    revenueEstimateFixed = None

                                    # fixes eps and epsEstimate string
                                    if company["eps"][0] == "(":
                                        epsFixed = Decimal(company["eps"][2:-1]) * -1
                                    elif company["eps"][0] == "$":
                                        epsFixed = Decimal(company["eps"][1:])

                                    if company["epsEstimate"][0] == "(":
                                        epsEstimateFixed = Decimal(company["epsEstimate"][2:-1]) * -1
                                    elif company["epsEstimate"][0] == "$":
                                        epsEstimateFixed = Decimal(company["epsEstimate"][1:])
                                    
                                    # appends all data to 2D list
                                    past_earnings.append([company["symbol"], company["name"], epsEstimateFixed, epsFixed, Decimal(str(company["revenueEstimate"])), Decimal(str(company["revenue"]))])
                    except:
                        continue

    
    text = "Past Earnings: \n"

    for company in past_earnings: # calculates surprise percentages and neatly displays past info
        if (company[2] and company[3] and company[4] and company[5]) and (company[2] != 0):
            epsPercent = (company[3] - company[2]) / abs(company[2]) * 100
            revenuePercent = (company[5] - company[4]) / abs(company[4]) * 100

            epsPercent = round(epsPercent, 2)
            revenuePercent = round(revenuePercent, 2)
        else:
            epsPercent = "DATA MISSING. Search online"
            revenuePercent = ""

        text += company[1] + " (" + company[0] + ") - EPS Beat/Miss: " + str(epsPercent) + "% - Revenue Beat/Miss: " + str(revenuePercent) + "%\n"

    text += "\nUpcoming Earnings: \n"

    for company in upcoming_earnings: # neatly displays upcoming info
        text += company[1] + " (" + company[0] + ") - Reporting on: " + company[2] + "\n"

    text += "\n"

    return text