from datetime import date
from google import genai
import time
from datetime import date
import numpy as np
import os
from dotenv import load_dotenv

# uses .env to access keys
load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY")

client = genai.Client(api_key=gemini_key) # preps Gemini client

dateForQuery = str(int(date.today().strftime('%Y%m%d')) - 1) + 'T1700' # gets proper date

def get_text(): # for summary text
    text = "Summary: \n"

    import requests

    # accesses all articles from past 24 hours about macro economy and financial markets
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=economy_macro,financial_markets&sort=RELEVANCE&time_from=' + dateForQuery + '&limit=1000&apikey=' + alpha_vantage_key
    r = requests.get(url)
    data = r.json()['feed']
    summaries = []

    for article in data: # decides which articles to keep
        relevance_combo = 0  # calculates how relevant each article is (sum of economic relevance and financial market relevance)
        movement_ability = 0 # calculates positive or negative sentiment ability
        
        for topic in (article["topics"]):
            if topic["topic"] == "economy_macro" or topic["topic"] == "financial_markets":
                relevance_combo += float(topic["relevance_score"])

            movement_ability = abs(float(article["overall_sentiment_score"]))

        if relevance_combo >= 1.675 and movement_ability > 0.375: # if relevance is strong and high movement potential
            summaries.append(article['summary']) # keep article

    summaries = np.unique(summaries) # remove duplicates

    # now, Gemini comes in handy
    prompt = "Summarize the following macroeconomic and market news into a concise daily briefing for a professional audience. Keep it 3-5 paragraphs and highlight only the most important developments. Avoid repeating details. No special heading is necessary, you can go immediately into the summary. \n\n"
    prompt += "\n\n".join(summaries)

    try: # prompts gemini to summarize all of the articles and returns neatly as text
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text += response.text
        text += "\n\n"

        return text
    except Exception as e:
        print("Error: ", e)
        return None

