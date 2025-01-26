import newspaper
from newspaper import Article
import yfinance as yf
import os
import csv
from datetime import datetime, timedelta
from functools import cache
import pandas as pd
from MasterLogic import master_input

# Persistent storage file for visited links
VISITED_LINKS_FILE = "visited_links.csv"

# Load visited links from file
def load_visited_links():
    if os.path.exists(VISITED_LINKS_FILE):
        with open(VISITED_LINKS_FILE, "r") as file:
            return set(row[0] for row in csv.reader(file))
    return set()

# Save a single visited link to file
def save_visited_link(link):
    with open(VISITED_LINKS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([link])

# Analyze the article (placeholder for actual implementation)
def analyze_article(title, text, publish_date, url, source_brand):
    # If CSV file is empty, add headers
    if not os.path.exists("news.csv") or os.stat('news.csv').st_size == 0:
        with open('news.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "text", "publish_date", "url", "source_brand"])
    
    # Save to CSV dataframe
    with open('news.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([title, text, publish_date, url, source_brand])
    
    # When we have 20 articles, call the run_model function
    df = pd.read_csv('news.csv')
    if len(df) >= 20:
        predictions = master_input(df)
        current = pd.read_csv('analysis.csv')
        merged = pd.concat([current, predictions], ignore_index=True)
        merged.to_csv('analysis.csv', index=False)
        # Clear the file
        open('news.csv', 'w').close()

# Process articles from a given source
def process_articles(source, visited_links):
    for article in source.articles:
        if article.url in visited_links:
            continue

        try:
            article.download()
            article.parse()

            # Add to visited links and save immediately
            visited_links.add(article.url)
            save_visited_link(article.url)

            # Call the analyze function
            analyze_article(
                title=article.title,
                text=article.text,
                publish_date=article.publish_date,
                url=article.url,
                source_brand=source.brand
            )
        except Exception as e:
            print(f"Failed to process article {article.url}: {e}")

@cache
def calculate_normalized_volume_change(ticker, target_date):
    # Fetch data for the last 7 days + the target date
    start_date = target_date - timedelta(days=7)
    end_date = target_date + timedelta(days=1)  # Include the target date

    # Fetch historical data
    stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)

    # Ensure data for the target date is available
    if target_date not in stock_data.index.date:
        raise ValueError(f"No data available for {ticker} on {target_date}")

    # Extract volume for the target date
    target_date_volume = stock_data.loc[stock_data.index.date == target_date, 'Volume'].iloc[0]

    # Calculate weekly average volume (excluding target date)
    weekly_data = stock_data.loc[stock_data.index.date != target_date, 'Volume']
    weekly_avg_volume = weekly_data.mean()

    # Calculate Normalized Relative Volume Change
    if weekly_avg_volume > 0:
        normalized_rvc = abs((target_date_volume - weekly_avg_volume) / weekly_avg_volume * 100)
    else:
        normalized_rvc = 0  # Avoid division by zero

    return normalized_rvc

@cache
def detect_price_anomalies(ticker, target_date):
    # Fetch data for the last 7 days + the target date
    start_date = target_date - timedelta(days=7)
    end_date = target_date + timedelta(days=1)  # Include the target date
    stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)

    # Ensure data for the target date is available
    if target_date not in stock_data.index.date:
        raise ValueError(f"No data available for {ticker} on {target_date}")

    # Extract data for the target date
    target_day = stock_data.loc[stock_data.index.date == target_date]
    target_open = target_day['Open'].iloc[0]
    target_close = target_day['Close'].iloc[0]

    # Calculate percentage price change
    absolute_change = target_close - target_open
    percentage_change = (absolute_change / target_open) * 100

    return {
        "Ticker": ticker,
        "Percentage Change (%)": percentage_change
    }

@cache
def calculate_combined_score(ticker, target_date):
    try:
        # Fetch volume anomaly
        volume_result = calculate_normalized_volume_change(ticker, target_date)

        # Fetch price anomaly
        price_result = detect_price_anomalies(ticker, target_date)

        # Metrics
        normalized_volume_change = volume_result
        percentage_price_change = price_result["Percentage Change (%)"]

        # Weights for volume and price
        w_v = 1  # Weight for volume
        w_p = 2  # Weight for price

        # Calculate combined score
        combined_score = (w_v * normalized_volume_change) + (w_p * percentage_price_change)

        return {
            "Ticker": ticker,
            "Normalized Volume Change": normalized_volume_change,
            "Percentage Price Change": percentage_price_change,
            "Combined Score": combined_score
        }
    except Exception as e:
        return {"Ticker": ticker, "Error": str(e), "Combined Score": 0}

def process_ticker_news(ticker, visited_links, max_articles=8):
    # Fetch ticker data
    stock = yf.Ticker(ticker)

    # Ensure the news attribute exists and is valid
    news_data = getattr(stock, 'news', None)
    if not news_data:
        print(f"No news data available for ticker: {ticker}")
        return {"Error": f"No news data available for ticker: {ticker}"}

    # Extract and process news articles, limit results to max_articles
    for article in news_data[:max_articles]:
        article_url = article.get("content", {}).get("canonicalUrl", {}).get("url", "No URL Available")
        if article_url == "No URL Available":
            continue

        # Check if the article has already been visited
        if article_url in visited_links:
            continue

        try:
            # Use Newspaper to fetch and parse article content
            news_article = Article(article_url)
            news_article.download()
            news_article.parse()

            news_item = {
                "title": news_article.title if news_article.title else article.get("content", {}).get("summary"),
                "text": news_article.text if news_article.text else article.get("content", {}).get("description"),
                "publish_date": datetime.strptime(article.get("content", {}).get("pubDate"), "%Y-%m-%dT%H:%M:%SZ"),
                "url": article_url,
                "source_brand": "Yahoo Finance",
            }
            analyze_article(**news_item)

            # Add to visited links and save
            visited_links.add(article_url)
            save_visited_link(article_url)

        except Exception as e:
            print(f"Failed to process article {article_url}: {e}")


# List of financial news sources
financial_news_sources = [
    # 'https://www.cnbc.com',                     # CNBC
    # 'https://www.reuters.com/finance',         # Reuters
    # 'https://www.bloomberg.com',               # Bloomberg
    # 'https://www.marketwatch.com',             # MarketWatch
    # 'https://www.ft.com/',                     # Financial Times
    # 'https://www.investing.com/',              # Investing.com
    # 'https://www.forbes.com/finance/',         # Forbes - Finance Section
    'https://www.theguardian.com/business',     # The Guardian - Business Section
]

stocks_data = pd.read_csv("stocks.csv", header=None)  # Assuming the file has no headers

# Extract tickers from the second column
stock_tickers = stocks_data.iloc[:, 1].dropna().astype(str).unique()

def main():
    # Adjust the target date as needed (e.g., two days ago)
    today = datetime.today().date() - timedelta(days=2)
    
    # Load visited links to avoid reprocessing
    visited_links = load_visited_links()
    print("Starting news scraping...")

    # Process general news sources (top financial news)
    for source_url in financial_news_sources:
        print(f"Processing source: {source_url}")
        try:
            source = newspaper.build(source_url, memoize_articles=False)
            process_articles(source, visited_links)
        except Exception as e:
            print(f"Failed to process source {source_url}: {e}")

    # Examine which stock tickers have anomalies based on high volumes of trade or price changes to prioritize news
    stock_tickers_sorted = sorted(
        stock_tickers,
        key=lambda ticker: calculate_combined_score(ticker, today).get("Combined Score", 0),
        reverse=True
    )
    
    print("\nStock tickers sorted by combined score:")
    for ticker in stock_tickers_sorted:
        score_info = calculate_combined_score(ticker, today)
        print(f"{ticker}: {score_info}")

    # Find news related to specific stock tickers
    for ticker in stock_tickers_sorted:
        print(f"\nProcessing stock ticker: {ticker}")
        try:
            process_ticker_news(ticker, visited_links, max_articles=8)
        except Exception as e:
            print(f"Failed to process stock ticker {ticker}: {e}")

    print("\nNews scraping complete.")

if __name__ == "__main__":
    main()
