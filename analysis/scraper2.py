import os
import csv
import time
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
from newspaper import Article

# Define the CSV file for storing news articles and visited URLs file
csv_file = "ticker_news_articles_2.csv"
visited_urls_file = "visited_urls_ticker_2.txt"

# Initialize columns for the DataFrame
columns = ["title", "text", "publish_date", "url", "source_brand"]

# Function to save data to CSV
def save_to_csv(data, file):
    try:
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file, index=False, mode='a', header=not os.path.exists(file), quoting=csv.QUOTE_ALL)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Function to load visited URLs
def load_visited_urls(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return set(line.strip() for line in f)
    return set()

# Function to save visited URLs
def save_visited_urls(urls, file):
    with open(file, "w") as f:
        f.writelines(f"{url}\n" for url in urls)

# Function to process news for a given ticker
def process_ticker_news(ticker, visited_urls, max_articles=8):
    stock = yf.Ticker(ticker)
    news_data = getattr(stock, 'news', None)
    if not news_data:
        print(f"No news data available for ticker: {ticker}")
        return []

    new_articles = []
    for article in news_data[:max_articles]:
        article_url = article.get("content", {}).get("canonicalUrl", {}).get("url", "No URL Available")
        if article_url in visited_urls or article_url == "No URL Available":
            continue
        
        eastern = pytz.timezone('US/Eastern')

        # Collecting news article data
        try:
            news_article = Article(article_url)
            news_article.download()
            news_article.parse()

            article_data = {
                "title": news_article.title if news_article.title else article.get("content", {}).get("summary"),
                "text": news_article.text if news_article.text else article.get("content", {}).get("description"),
                "publish_date": datetime.strptime(article.get("content", {}).get("pubDate"), "%Y-%m-%dT%H:%M:%SZ").astimezone(eastern),
                "url": article_url,
                "source_brand": "Yahoo Finance",
            }
            new_articles.append(article_data)
            visited_urls.add(article_url)
        except Exception as e:
            print(f"Error processing article {article_url}: {e}")

    return new_articles

# Load visited URLs
visited_urls = load_visited_urls(visited_urls_file)

# Process news for each ticker in the CSV file
all_new_articles = []
stocks_data = pd.read_csv("stocks.csv", header=None)  # Assuming the file has no headers

# Extract tickers from the second column
tickers = stocks_data.iloc[:, 1].dropna().astype(str).unique()

for ticker in tickers:
    print(f"Processing news for ticker: {ticker}")
    new_articles = process_ticker_news(ticker, visited_urls)
    all_new_articles.extend(new_articles)

    # Save newly visited URLs and articles periodically
    save_visited_urls(visited_urls, visited_urls_file)
    save_to_csv(new_articles, csv_file)
    # time.sleep(1)  # To avoid overwhelming servers

print("News processing and saving completed.")
